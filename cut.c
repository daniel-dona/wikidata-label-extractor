#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>

#define COPY_SIZE 1024*1024


int main(int argc, char **argv){

    if(argc != 5){

		printf("Wrong number of parameters!\n\nUse:\n\t cuttl [parts] [TTL file] [FIFO(s) name(s)]");

		exit(1);

    }

    int p = atoi(argv[1]);
    int fd = open(argv[2], O_RDWR);
    char * fifo_name = malloc(sizeof(char)*256);
    int pid, pypid;

    struct stat statbuf;
    fstat(fd, &statbuf);
    void * ptr = mmap(NULL, statbuf.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);


	for(int n = 1; n <= p; n++){
		
		sprintf(fifo_name, "%s.%d", argv[3], n);

		long start = (statbuf.st_size / p) * (n-1);
		long end = (statbuf.st_size / p) * n;

		printf("From %ld byte to %ld byte on FIFO %s\n", start, end, fifo_name);
			
		char b1, b2;
		
		for(long i = start; i < end && i != 0; i+=sizeof(char)){

			b1 = *((char*) (ptr+i));
			b2 = *((char*) (ptr+i+(sizeof(char))));

			if(b1 == '.' && b2 == '\n'){

				start = i+(sizeof(char)*2);
				break;

			}

		}
		
		
		for(long i = end; i < statbuf.st_size; i+=sizeof(char)){

			b1 = *((char*) (ptr+i));
			b2 = *((char*) (ptr+i+(sizeof(char))));

			if(b1 == '.' && b2 == '\n'){

				end = i+(sizeof(char)*2);
				break;

			}

		}
		
		mkfifo(fifo_name, 0666);
		
		printf("Spawning FIFO %d...\n", n);
		
		pid = fork();
		
		long int l_print = 0;
		int l_newl = 0;
		
		if(pid == 0){
			
			pypid = fork();
			
			if(pypid == 0){
		
				fd = open(fifo_name, O_WRONLY); 
				
				for(long i = start; i < end; i+=sizeof(char)*(COPY_SIZE)){

				
					if((end - i) < sizeof(char)*(COPY_SIZE)){
												
						write(fd, ((char*) ptr+i), sizeof(char)*((end) - i));
						
						break;
						
					}else{
						
						write(fd, ((char*) ptr+i), sizeof(char)*(COPY_SIZE));
						
					}
					
					if(time(NULL) > (l_print+2)){
						
						printf("[ %d %.2f%% ]", n,  ((float) (i-start)/ (float) (end-start))*100);
						
						fflush(stdout);
						
						l_print = time(NULL);
						l_newl = 0;
						
					}
					
					if(time(NULL) > (l_print+1) && n == 1 && l_newl == 0){
						
						l_newl = 1;
						printf("\n");
						
					}
						

				}

				printf("\nFIFO %d finished!", n);
				
				close(fd);
				
				exit(0);
				
			}else{
				
				char * tsv_name = malloc(sizeof(char)*256);
				
				sprintf(tsv_name, "%s.%04d", argv[4], n);
				
				char * pyargs[] = {"/usr/bin/python3", "extract.py", fifo_name, tsv_name, NULL};
				
				execvp(pyargs[0],pyargs);

			}
		
		}else{
			
			printf("\tPID: %d\n\n", pid);
			
		}
		
	}
	
	for(int i = 0; i < p; i++){
		
		printf("\n%d ended...\n", wait(NULL));

	}

    exit(0);

}
