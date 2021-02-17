let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd /var/www/src/front/src
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +81 /etc/nginx/nginx.conf
badd +11 /etc/nginx/sites-enabled/assetmanager.conf
badd +1 js/assets/get_assets.js
badd +12 js/locations/get_locations.js
badd +10 js/pictures/get_pictures.js
badd +9 js/user/check_login.js
badd +13 js/user/tokens.js
badd +7 js/config.js
badd +2 components/NavBar.vue
badd +59 /var/www/src/front/package.json
argglobal
%argdel
$argadd js/assets/get_assets.js
$argadd js/assets/query_params.js
$argadd js/locations/get_locations.js
$argadd js/pictures/get_pictures.js
$argadd js/user/check_login.js
$argadd js/user/tokens.js
edit js/config.js
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
if bufexists("js/config.js") | buffer js/config.js | else | edit js/config.js | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 7 - ((4 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 0
lcd /var/www/src/front/src
tabnext 1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOF
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
