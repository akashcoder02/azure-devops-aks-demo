output "vm_names" {
  value = [
    for vm in module.vm : vm.vm_name
  ]
}

output "public_ips" {
  value = [
    for vm in module.vm : vm.public_ip
  ]
}

output "private_ips" {
  value = [
    for vm in module.vm : vm.private_ip
  ]
}