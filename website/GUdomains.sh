#!/bin/bash

echo "Cleaning previous build..."
rm -rf Soccer-Data-API

echo "Rendering Quarto website..."
quarto render

echo "Setting permissions..."

find Soccer-Data-API -type f -exec chmod 644 {} \;
find Soccer-Data-API -type d -exec chmod 755 {} \;

read -p "Deploy website to GU Domains? (y/n): " answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then

    echo "Deploying website..."

    scp -r Soccer-Data-API corcoran@corcoran.georgetown.domains:/home/corcoran/public_html/

    echo "Deployment complete."

else

    echo "Deployment skipped."

fi