r=$(curl 'http://travian.kirilloid.ru/awar2.php' \
  -H 'Accept: application/json' \
  -H 'Accept-Language: it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6,ar;q=0.5' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-type: application/x-www-form-urlencoded' \
  -H 'Cookie: dpi=96; _ga=GA1.2.493928063.1650902197; show_surv=; _gid=GA1.2.520603616.1652092431; _gat=1' \
  -H 'Origin: http://travian.kirilloid.ru' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://travian.kirilloid.ru/warsim2.php' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36' \
  --data-raw 'data=[{"p":500,"r":3},{"r":3,"u":[30,20,0,0,8,0,0,0,0,0],"U":[0,0,0,0,0,0,0,0],"side":"def"},{"r":1,"R":1,"u":[0,0,0,0,0,400,0,0,0,0],"U":[0,0,0,0,0,15,0,0],"b":[0,0],"side":"off"}]&mode=9' \
  --compressed \
  --insecure \
  -s )

echo $r