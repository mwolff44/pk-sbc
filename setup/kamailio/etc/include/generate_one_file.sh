#find . -type f -name '*.cfg' -exec cat {} + > ../kamailio.cfg
cat $(find . -type f -name '*.cfg' | sort -V) > ../kamailio.cfg
echo 'PyFB v3.0 - file version : '$(date +"%Y-%m-%d %H:%M:%S") | cat - ../kamailio.cfg > temp && mv temp ../kamailio.cfg
