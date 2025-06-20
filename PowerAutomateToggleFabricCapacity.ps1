# on the automation account this is done through the portal/cli
# Install-Module -Name Az.Fabric -RequiredVersion 0.1.2 -Force
# Import-Module Az.Fabric 

# Connect using Managed Identity
Connect-AzAccount -Identity

# Parameters
$resourceGroup = "<resource_group>"
$capacityName  = "<capacity_name>"
$subId         = (Get-AzContext).Subscription.Id

# Check current state
$cap = Get-AzFabricCapacity -ResourceGroupName $resourceGroup -CapacityName $capacityName -SubscriptionId $subId
$state = $cap.State  # e.g., 'Succeeded' or 'Paused'
Write-Output "Current Fabric capacity state: $state"

# 4. Suspend or resume based on state
if ($state -eq 'Succeeded') {
    Write-Output "⏸ Suspending capacity..."
    Suspend-AzFabricCapacity -ResourceGroupName $resourceGroup -CapacityName $capacityName -SubscriptionId $subId -NoWait
    Write-Output "📨 Suspend operation started."
}
elseif ($state -eq 'Paused') {
    Write-Output "▶ Resuming capacity..."
    Resume-AzFabricCapacity -ResourceGroupName $resourceGroup -CapacityName $capacityName -SubscriptionId $subId -NoWait
    Write-Output "📨 Resume operation started."
}
else {
    Write-Output "⚠ Unknown state '$state'. No action taken."
}
