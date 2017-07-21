#include <windows.h>
#include <iostream>
#include<string>
using namespace std;
typedef string (*preditFunc)(const string & img_file);
int main(int argc, char *argv[])
{
	HMODULE hDll = LoadLibrary("FaceEmotionDLL.dll");
	if (hDll != NULL)
	{
		preditFunc preditFirst = (preditFunc)GetProcAddress(hDll, "preditFirst");
		if (preditFirst != NULL)
		{
			string img = "sad978.png";
			if (argc > 1) {
				img = argv[1];
			}
			string result = preditFirst(img);
			cout << "result : " << result;
		}
		FreeLibrary(hDll);
	}
}