"""

Have a good time reading the source. You are an amazing person.

"""

from colorama import Fore, Style
import colorama, random

colorama.init()

banner = Style.BRIGHT + Fore.CYAN + r"""
        ___     ____    ____    ____    ___     ____    _  _    _    ____
        |__]    |__|    |__/    |__|    |  \    |  |     \/     |    |__| 
        |       |  |    |  \    |  |    |__/    |__|    _/\_    |    |  |  
                     
        -----------------------------  -------------------------------   
                             Control is an Illusion                                                      
""" + Style.RESET_ALL

bannertwo = Style.BRIGHT + Fore.YELLOW + r"""
                                 ______________
                           ,===:'.,            `-._
                                `:.`---.__         `-._
        Never tell everything     `:.     `--.         `.
           you know...              \.        `.         `.
                                    (,,(,    \.         `.   ____,-`.,
                         (,'     `/   \.   ,--.___`.'
                     ,  ,'  ,--.  `,   \.;'         `
                      `{D, {    \  :    \;
                        V,,'    /  /    //
                        j;;    /  ,' ,-//.    ,---.      ,
                        \;'   /  ,' /  _  \  /  _  \   ,'/
                              \   `'  / \  `'  / \  `.' /
                               `.___,'   `.__,'   `.__,'  
                                                        """ + Style.RESET_ALL

bannerthree = Style.BRIGHT + Fore.BLUE + r"""

       |,---"-----------------------------"---,|
       ||paradoxia> cat loot/xx/tasklist      ||
       ||Image Name   			      ||
       ||==========================           ||
       ||System   			      ||
       ||chrome.exe			      ||
       ||winsvchost.exe		              ||
       ||       			      ||
       ||_____,_________________________,_____||
       |)_____)-----.| -------- |.------(_____(|
     //''''''|_____|=----------=|______|'''''''\\
    // _| _| _| _| _| _| _| _| _| _| _| _| _| _| \
   // ___| _| _| _| _| _| _| _| _| _| _| _|  |  | \
  |/ ___| _| _| _| _| _| _| _| _| _| _| _| ______| \
  / __| _| _| _| _| _| _| _| _| _| _| _| _| _| ___| \
 / _| _| _| _| ________________________| _| _| _| _| \
|----------------------------------------------------|
`-----------------------------------------------------'		
						""" + Style.RESET_ALL


bannerfour = Style.BRIGHT + Fore.RED + r"""

                        _--_
                       /   -)
                   ___/___|___
      ____-----=~~///|     ||||~~~==-----_____
    //~////////////~/|     |//|||||\\\\\\\\\\\\\
  ////////////////////|   |///////|\\\\\\\\\\\\\\\
 /////~~~~~~~~~~~~~~~\ |.||/~~~~~~~~~~~~~~~~~`\\\\\
//~                  /\\|\\                      ~\\
                    ///W^\W\
                   ////|||\\\
                   ~~~~~~~~~~
Injustice anywhere is a threat to Justice everywhere.

""" + Style.RESET_ALL
bannerfive = Style.BRIGHT + Fore.LIGHTGREEN_EX + r'''

    .o oOOOOOOOo                                            OOOo
    Ob.OOOOOOOo  OOOo.      oOOo.                      .adOOOOOOO
    OboO"""""""""""".OOo. .oOOOOOo.    OOOo.oOOOOOo.."""""""""'OO
    OOP.oOOOOOOOOOOO "POOOOOOOOOOOo.   `"OOOOOOOOOP,OOOOOOOOOOOB'
    `O'OOOO'     `OOOOo"OOOOOOOOOOO` .adOOOOOOOOO"oOOO'    `OOOOo
    .OOOO'            `OOOOOOOOOOOOOOOOOOOOOOOOOO'            `OO
    OOOOO                 '"OOOOOOOOOOOOOOOO"`                oOO
   oOOOOOba.                .adOOOOOOOOOOba               .adOOOOo.
  oOOOOOOOOOOOOOba.    .adOOOOOOOOOO@^OOOOOOOba.     .adOOOOOOOOOOOO
 OOOOOOOOOOOOOOOOO.OOOOOOOOOOOOOO"`  '"OOOOOOOOOOOOO.OOOOOOOOOOOOOO
 "OOOO"       "YOoOOOOMOIONODOO"`  .   '"OOROAOPOEOOOoOY"     "OOO"
    Y           'OOOOOOOOOOOOOO: .oOOo. :OOOOOOOOOOO?'         :`
    :            .oO%OOOOOOOOOOo.OOOOOO.oOOOOOOOOOOOO?         .
    .            oOOP"%OOOOOOOOoOOOOOOO?oOOOOO?OOOO"OOo
                 '%o  OOOO"%OOOO%"%OOOOO"OOOOOO"OOO':
                      `$"  `OOOO' `O"Y ' `OOOO'  o             .
    .                  .     OP"          : o     .
                              :
                              .
    A Devil is at his strongest when we are looking the other way,
    like a program running in the background silently, while we are busy doing
    other shit.        
''' + Style.RESET_ALL
def pbanner():
    return random.choice([banner, bannertwo, bannerthree, bannerfour, bannerfive])
