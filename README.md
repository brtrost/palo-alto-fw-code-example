  Brian Trost, trostb@gmail.com

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

