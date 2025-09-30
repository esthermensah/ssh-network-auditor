# Vagrantfile
Vagrant.configure("2") do |config|
  # Use the official Kali Linux rolling image from Vagrant Cloud
  config.vm.box = "kalilinux/rolling"

  # Define the first VM (server)
  config.vm.define "kali-server" do |server|
    server.vm.hostname = "kali-server"
    server.vm.network "private_network", ip: "192.168.56.101"
    server.vm.provider "virtualbox" do |vb|
      vb.name = "Kali_Server_VM2"
      vb.memory = "1024"
      vb.cpus = 1
    end
  end

  # Define the second VM (client)
  config.vm.define "kali-client" do |client|
    client.vm.hostname = "kali-client"
    client.vm.network "private_network", ip: "192.168.56.102"
    client.vm.provider "virtualbox" do |vb|
      vb.name = "Kali_Client_VM2"
      vb.memory = "1024"
      vb.cpus = 1
    end
  end
end
