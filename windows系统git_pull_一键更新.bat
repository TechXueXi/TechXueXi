@echo off
goto start


:color_red
echo [31m[*] %1[0m
exit /b 0

:color_green
echo [32m[*] %1[0m
exit /b 0

:color_yellow
echo [33m[*] %1[0m
exit /b 0

:color_blue
echo [34m[*] %1[0m
exit /b 0

:replace_dir
call :color_yellow ÖØÒªĞÅÏ¢£º
echo ´ËÄ¿Â¼ÒÑ×÷·Ï£¬Çë×ªµ½ TechXuexi-master-clone Ä¿Â¼
echo ÒÑ×Ô¶¯ÎªÄú¸´ÖÆ user ÎÄ¼ş¼ĞºÍ chrome ÎÄ¼ş¼Ğ£¬´ËÎªÓÃ»§Êı¾İ£¬
echo Îª±£Ö¤ÎŞÎóÄú¿ÉÔÙÈ·ÈÏÒ»ÏÂÄ¿Â¼ÄÚÊÇ·ñÒÑ¾­ÓĞÕâÁ½¸öÎÄ¼ş¼Ğ
echo Äú¿É½« TechXuexi-master-clone ÀïµÄËùÓĞÄÚÈİ£¨º¬.gitÎÄ¼ş¼Ğ£©Ìæ»»´ËÎÄ¼ş¼ĞµÄËùÓĞÄÚÈİ
exit /b 0


:start
set repo_url1=https://hub.fastgit.xyz/TechXueXi/TechXueXi.git
set repo_url2=https://hub.fastgit.org/TechXueXi/TechXueXi.git
set push_url=git@github.com:TechXueXi/TechXueXi.git

if exist "_unavailable_dir" (
	call :replace_dir
	goto end
)

:enter_file_path
set file_path=%~dp0
%file_path:~0,1%:
cd "%file_path%"

:test_have_git
call :color_green ¼ì²é´ËµçÄÔÓĞÎŞ°²×°git
git --version
if %ERRORLEVEL% equ 0 (
    goto have_git
) else (
    goto not_have_git
)

:have_git
:test_is_git_repo
call :color_green ¼ì²é´ËÎÄ¼ş¼ĞÊÇ·ñÊÇgit¿â
git remote -v
if %ERRORLEVEL% equ 0 (
    goto is_a_repo
) else (
    goto git_init
)

:is_a_repo
call :color_green ÏÖÔÚ¼ì²éremoteµØÖ·ÉèÖÃ
git remote -v >nul 2>nul
git config remote.origin.url %repo_url1%
git config remote.origin.pushurl %push_url%
git remote -v
call :color_green À­È¡Ô¶³Ì´úÂë£¨ÈçÔÚ´Ë¿¨×¡10ÃëÒÔÉÏ¿É¹Ø±ÕÖØĞÂ´ò¿ª£©
git fetch
call :color_green Ôİ´æĞŞ¸Ä
git stash save "pull_auto_stash"
call :color_green ¸üĞÂ...£¨ÈçÔÚ´Ë¿¨×¡10ÃëÒÔÉÏ¿É¹Ø±ÕÖØĞÂ´ò¿ª£©
git pull --rebase
call :color_green »Ö¸´ĞŞ¸Ä
git stash pop
git checkout windowsÏµÍ³git_pull_Ò»¼ü¸üĞÂ.bat
call :color_green Íê³É
goto end


:git_init
call :color_green ÏÂÔØ×îĞÂ´úÂëµ½TechXuexi-master-cloneÎÄ¼ş¼Ğ
git clone -b master %repo_url1% TechXuexi-master-clone
if %ERRORLEVEL% equ 0 (
	call :color_green ¸´ÖÆÓÃ»§Êı¾İÎÄ¼ş...
	xcopy /E /V /K /I /Y /Q SourcePackages\user TechXuexi-master-clone\SourcePackages\user
	xcopy /E /V /K /I /Y /Q SourcePackages\chrome TechXuexi-master-clone\SourcePackages\chrome
	echo. >_unavailable_dir
	call :color_green Íê³É.
	call :replace_dir
	goto end
) else (
	call :color_red ³öÏÖ´íÎó£¡Çë·´À¡´ËÎÊÌâ£ºgit_clone_³ö´í
	goto end
)

:not_have_git
call :color_yellow ÕÒ²»µ½git£¬Çë×ÔĞĞËÑË÷°²×°gitºóÔÙ´ò¿ªÔËĞĞ¡£
goto end




:end
set/p=°´»Ø³µ¼üÍË³ö³ÌĞò...

