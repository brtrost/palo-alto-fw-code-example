  Brian Trost, trostb@gmail.com

  python panfw-base-script.py

    This script is a template that can be used for Palo Alto API scripting using Python.

  python show-arp.py -f x.x.x.x -i ae3.125

    Displays arp output of a single firewall or interface.  Script can be modified to do other op commands from the firewall.

    This script must be able to access the management firewall interface of the firewall.
    ----------
    show-arp.py - show arp with cleaned up output

    Total arp entries: 2

    10.x.x.124 - xx:xx:xx:45:72:c7 - ae9.45 - 824
    10.x.x.126 - xx:xx:xx:67:22:57 - ae9.45 - 579

  python connect-to-fw-through-pano.py -f x.x.x.x

    Connects to a target, checks if it is Panorama.  Then it queries all connected firewalls and displays all VSYS entries.
    ----------
    connect-to-fw-through-pano.py - show devices and check zone settings

    Querying device x.x.x.x

    Firewall1 - 007xxxxxxxxx - 192.168.1.1 - PA-5060

     Finding VSYS
     - Found VSYS entry vsys1 - DEPT1
     - Found VSYS entry vsys2 - DEPT2

     Firewall2 - 007xxxxxxxxx - 192.168.1.2 - PA-7080

  retkey.py

   This file can be 'import'ed and retrieves a API key from the user's home directory in .panconfkeystore.  Can be useful so one doesn't have to store API keys a program.  The source file can be changed and is expecting text in the '<ip>:<apikey>' format with one per line.  This file is the PAN-C API key storage location.

     try:
         import retkey
     except:
         pass

     try:
         retkey.read_key_file("x.x.x.x")
     except:
         apikey = args.apikey    # If you're passing by args  
