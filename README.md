## RainFall

Reverse binaries and find exploits

[Download image](https://projects.intra.42.fr/uploads/document/document/5638/RainFall.iso) (Ubuntu Linux)

[More information about project in subject file.](https://cdn.intra.42.fr/pdf/pdf/33547/en.subject.pdf)

### Prepare

Break process is automated, at first obtain dependencies

You need CLI:
- Sshpass

For MacOS (Install deps from brew and python deps by pip3):

```shell
./install
```

CLI deps standalone:

**Use a package manager for your system** 

Python deps standalone:

```shell
pip3 install -r requirements.txt
```

### Usage

- Edit utils/config.py and specify VM host and port

You can delete all flag files for the purity of the experiment flags will be writen after level successfully broken
```shell
./remove_flags
```

You can run break process for all levels together, step by step

```shell
./break_all
```

Run one by one, e.g.
```shell
cd level09/Ressources && python3 break.py
```

Or run step by step by Jupyter, e.g.
```shell
cd level09 && ./preview
```
