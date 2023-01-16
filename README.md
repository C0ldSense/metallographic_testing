

  <p align="center">
    Welcome to the repository!
    <br />
    <br />
    <br />
    <a href="https://github.com/C0ldSense/metallographic_testing/issues">Report Bug</a>
    ·
    <a href="https://github.com/C0ldSense/metallographic_testing/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

Metallographic testing of additive printed objects. This script should analyze given specimen of additve printed cubes.


### Built With

Programming Language: <a href="https://www.python.org/downloads/release/python-3916/">Python [Version 3.9.16]</a> 
<br>Flashing Software: <a href="https://downloads.raspberrypi.org/imager/imager_latest.exe">Rasperry Pi Imager</a>
<br>Operating System: <a href="https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2022-09-26/2022-09-22-raspios-bullseye-arm64.img.xz">Raspberry Pi OS [Kernel version: 5.15]</a> 







<!-- GETTING STARTED -->
## Getting Started

- Step 1: Create Pi credentials in the Raspebrry Pi Imager (example):
  - Hostname: LabPi
  - Choose: [SSH aktivieren - Passwort zur Authentifizierung verwenden]
  - Choose: [Benutzername und Passwort setzen]
    - Username: LabPi
    - Password: Raspberry

- Step 2: Flash Raspberry Pi OS to the SD Card
  - Make sure login credentials have been set before flashing!

- Step 3: Raspberry Pi headless start
  - Connect with "ssh LabPi@LOCALIPFROMPI"
  - Change knownhosts if necessary
  - Confirm with "yes"
  - Confirm password 

- Step 4: Git Setup
  - ``` sudo apt install git ```
  - ``` mkdir Git ``` 
  - ``` cd Git ``` 
  - ``` ssh keygen ``` (leave name and password empty)
  - ``` cat ~/.ssh/id_rsa.pub ``` 
  - Copy RSA key and add do Github
  - ```git clone git@github.com:C0ldSense/metallographic_testing.git```
  - ```cd metallographic_testing```
  - ```git pull```
  - Optional: ```git checkout ``` for changing branch
  
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* You need to install these:
  ```
  pip install matplotlib opencv-python
  
  sudo apt-get install python3-pil python3-pil.imagetk python-tk
  ```

### How to start

1. Locate script.py
2. Start script with    
   ```
   python script.py
   ```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[python-shield]: https://upload.wikimedia.org/wikipedia/commons/1/1b/Blue_Python_3.9_Shield_Badge.svg
[python-url]:https://www.python.org/
