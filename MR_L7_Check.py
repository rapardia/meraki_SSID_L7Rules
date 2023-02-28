import meraki
import csv

key = input('Enter API Key: ')

dashboard = meraki.DashboardAPI(key)

#Get Meraki Organization ID
def get_org():
    global org_id
    response = dashboard.organizations.getOrganizations()
    org_id = response[0]['id']

#Get L7 Rules For each SSID in Organization
def get_rules():
    #Get list of Networks in Org
    response = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
    #Open/Create CSV for editing
    with open("L7_Rules.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Network','SSID','L7 Rules'])
        #Inlude only Networks with Wireless Products
        for i in response:
            net_id = i['id']
            net_name = i['name']
            net_type = i['productTypes']
            if 'wireless' in net_type:
                #Get List of SSIDs for each Network
                ssids = dashboard.wireless.getNetworkWirelessSsids(net_id)
                #Get L7 Rules for each SSID
                for m in ssids:
                    ssid_num = m['number'] 
                    ssid_name = m['name']
                    #Exclude SSIDs that with "Unconfigured" in name
                    if 'Unconfigured' in ssid_name:
                        pass
                    else:
                        l7_rule = dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(net_id, ssid_num)
                        rule = l7_rule['rules']
                        #Write Rules to CSV file
                        writer.writerow([net_name,ssid_name,rule])
            else:
                pass

def main():
    get_org()
    get_rules()

main()