#!/usr/bin/env sh

WKHTML2PDF_VERSION='0.12.5'

sudo apt-get install -y openssl build-essential xorg libssl-dev
wget "https://github.com/wkhtmltopdf/wkhtmltopdf/archive/${WKHTML2PDF_VERSION}.tar.gz"
https://github.com/wkhtmltopdf/wkhtmltopdf/archive/0.12.5.tar.gz
tar -xJf "wkhtmltox-${WKHTML2PDF_VERSION}.tar.xz"
cd wkhtmltox
sudo chown root:root bin/wkhtmltopdf
sudo cp -r * /usr/