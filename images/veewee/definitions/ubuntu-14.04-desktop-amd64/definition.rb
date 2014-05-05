Veewee::Session.declare({
  :cpu_count => '1',
  :memory_size=> '512',
  :disk_size => '10140',
  :disk_format => 'VDI',
  :hostiocache => 'off',
  :os_type_id => 'Ubuntu_64',
#
# ARGONNE MIRROR DESKTOP
  :iso_file => "ubuntu-14.04-desktop-amd64.iso",
  :iso_src => "http://mirror.mcs.anl.gov/pub/ubuntu-iso/CDs/14.04/ubuntu-14.04-desktop-amd64.iso",
  :iso_md5 => '0bc7243aacd5f80f8110dcf3165dffd0',
#
#UBUNTU MIRROR Deskptop
#
#  :iso_file => "ubuntu-14.04-desktop-amd64.iso",
#  :iso_src => "http://releases.ubuntu.com/14.04/ubuntu-14.04-desktop-amd64.iso",
#  :iso_md5 => 'dccff28314d9ae4ed262cfc6f35e5153',
  :iso_download_timeout => "1000",
  :boot_wait => "4",
  :boot_cmd_sequence => [
    '<Esc><Esc><Enter>',
    '/install/vmlinuz noapic preseed/url=http://%IP%:%PORT%/preseed.cfg ',
    'debian-installer=en_US auto locale=en_US kbd-chooser/method=us ',
    'hostname=%NAME% ',
    'fb=false debconf/frontend=noninteractive ',
    'keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA keyboard-configuration/variant=USA console-setup/ask_detect=false ',
    'initrd=/install/initrd.gz -- <Enter>'
],
  :kickstart_port => "7122",
  :kickstart_timeout => "10000",
  :kickstart_file => "preseed.cfg",
  :ssh_login_timeout => "10000",
  :ssh_user => "vagrant",
  :ssh_password => "vagrant",
  :ssh_key => "",
  :ssh_host_port => "7222",
  :ssh_guest_port => "22",
  :sudo_cmd => "echo '%p'|sudo -S sh '%f'",
  :shutdown_cmd => "shutdown -P now",
  :postinstall_files => [
    "base.sh",
    "vagrant.sh",
    "virtualbox.sh",
    "chef.sh",
    "cleanup.sh",
    "zerodisk.sh"
  ],
  :postinstall_timeout => "10000"
})
