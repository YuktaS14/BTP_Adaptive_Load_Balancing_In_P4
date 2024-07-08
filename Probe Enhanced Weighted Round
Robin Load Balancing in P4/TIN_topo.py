from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

net.setLogLevel('info')

# net.addP4RuntimeSwitch('s1', cpu_port = 555)
net.addP4Switch('s1')

# net.log
net.addHost('c1')
net.addHost('v1')
net.addHost('v2')
#net.addHost('h3', ip='10.0.3.3/24', mac='08:00:00:00:03:33')
#net.addP4Switch('s2')
#net.addP4Switch('s3')
# net.addHost('v3')
# net.enableCpuPort('s1');


net.setP4Source('s1','fd.p4')
#net.setP4Source('s2','fd.p4')
#net.setP4Source('s3','fd.p4')

# net.setP4CliInput('s1', './s1-commands-stateless.txt')
# net.setP4CliInput('s1', './entries1.txt')
#net.setP4CliInput('s3', './entries3.txt')

net.addLink('c1', 's1')
net.addLink('v1', 's1')
net.addLink('v2', 's1')
#net.addLink('h3', 's3')
#net.addLink('s1', 's2')
#net.addLink('s1', 's3')
#net.addLink('s2', 's3')

# net.addLink('v1', 'v3')

# net.setIntfPort('v1','v3', 1)
# net.setIntfPort('v3','v1', 0)


net.setIntfPort('s1', 'c1', 1)
net.setIntfPort('s1', 'v1', 2)  # Set the number of the port on s1 facing h1
net.setIntfPort('s1', 'v2', 3)  # Set the number of the port on s1 facing h1
net.setIntfPort('v1', 's1', 0)  # Set the number of the port on h1 facing s1
net.setIntfPort('c1', 's1', 0)
net.setIntfPort('v2', 's1', 0)

#net.setIntfPort('s2', 'h2', 1)  # Set the number of the port on s1 facing h2
#net.setIntfPort('h2', 's2', 0)  # Set the number of the port on h2 facing s1
#net.setIntfPort('s3', 'h3', 1)  # Set the number of the port on s1 facing h3
#net.setIntfPort('h3', 's3', 0)  # Set the number of the port on h3 facing s1
#net.setIntfPort('s1', 's2', 2)
#net.setIntfPort('s2', 's1', 2)
#net.setIntfPort('s2', 's3', 3)
#net.setIntfPort('s3', 's2', 3)
#net.setIntfPort('s1', 's3', 3)
#net.setIntfPort('s3', 's1', 2)

# net.setBw('s1','h1', 5)
# net.setBwAll(5)
net.l2()
net.enablePcapDumpAll()
#net.setb

net.enableLogAll()
net.enableCli()
net.startNetwork()
