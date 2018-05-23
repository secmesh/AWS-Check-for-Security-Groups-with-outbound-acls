import boto3
import boto
import boto.utils
from boto.vpc import VPCConnection


client = boto3.client("ec2")
conn=boto.vpc.connect_to_region("us-west-2")

##Below lines will connect to the vpc and look at the instaces (by instance IDs)##

tag_list={}
grp_list=list()
reservations = conn.get_all_reservations()
for r in reservations:
    for inst in r.instances:
        for group in inst.groups:
            response = client.describe_security_groups(
                     GroupIds=[
                     group.id,
                  ],
                )

##Below lines will look for the security groups in the AWs environment and check for valid outbound ACLS (excluding allow any) and print them out with the Group Name##

            for i in response['SecurityGroups']:
              if 'IpPermissionsEgress'in i:
                for l in i['IpPermissionsEgress']:
                  lst=list()
                  final_lst=list()
                  if '-1' in l['IpProtocol']:
                   lst.append(l['IpProtocol'])
                  for i in l['IpRanges']:
                    if '0.0.0.0/0' in i['CidrIp']:

                     lst.append(i['CidrIp'])
                     break
                  if '-1' and '0.0.0.0/0' in lst: break
                  else:
                     final_lst.append(group.id)
                  for i in inst.tags:
                    if 'Name' not in i:continue
                    else:
                       if not final_lst:break
                       else:
                           tag_list[inst.tags['Name']]=final_lst
                  print tag_list


for k,v in tag_list.items():
    print k,v

