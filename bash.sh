sudo apt-get update
sudo apt install python3-pip
pip install -r requirements.txt
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update 
sudo apt install google-chrome-stable
apt install libxss1
sudo apt install fonts-wqy-zenhei
sudo apt-get install chromium-chromedriver