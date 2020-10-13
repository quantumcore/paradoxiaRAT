COMPILER 				:=
ifeq ($(OS),Windows_NT)
	COMPILER += gcc
else
	COMPILER += i686-w64-mingw32-gcc
endif

WINDRES 				:=
ifeq ($(OS),Windows_NT)
	WINDRES += windres
else
	WINDRES += i686-w64-mingw32-windres
endif


OUTFILE := {{outfilehere}}

main:
	$(COMPILER) main.c paradoxia.c ParadoxiaClient.c sys.c LoadLibraryR.c GetProcAddressR.c  -o $(OUTFILE) -lws2_32 -static -liphlpapi -m32 -mwindows  -lwinmm -lpsapi -lwininet -lshlwapi -MD -s -O3
make icon:
	$(WINDRES) icon.rc -O coff -o icon.res -F pe-i386
	$(COMPILER) main.c paradoxia.c ParadoxiaClient.c sys.c LoadLibraryR.c GetProcAddressR.c  -o $(OUTFILE) icon.res -lws2_32 -static -liphlpapi -m32 -mwindows  -lwinmm -lpsapi -lwininet -lshlwapi -MD -s -O3
clean:
	$(del) *.d
	$(del) *.exe
	