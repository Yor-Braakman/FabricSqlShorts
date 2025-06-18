# Connect using Managed Identity
Connect-AzAccount -Identity

# Variables
$resourceGroup = "<resource_group>"
$capacityName  = "<capacity_name>"
$resourceType  = "Microsoft.Fabric/capacities"
$apiVersion    = "2023-11-01"

$capacity = Get-AzResource -ResourceGroupName $resourceGroup `
                           -ResourceType $resourceType `
                           -ResourceName $capacityName `
                           -ApiVersion $apiVersion `
                           -ErrorAction SilentlyContinue

if (-not $capacity) {
    Write-Output "❌ ERROR: Could not find the Fabric capacity resource."
    return
}

# Output the full JSON for inspection
# Write-Output "🔍 Dumping full Fabric capacity resource JSON:"
# $capacity | ConvertTo-Json -Depth 10 | Out-String | Write-Output

$state = $capacity.Properties?.status

if (-not $state) {
    Write-Output "❌ ERROR: status not found on the resource."
    return
}

Write-Output "✅ Current capacity status: $state"

# --- Helper: Invoke REST method to resume or suspend ---
function Invoke-CapacityAction {
    param (
        [string]$action  # "resume" or "suspend"
    )

    $token = (Get-AzAccessToken).Token
    $resourceId = $capacity.ResourceId.TrimEnd('/')
    $uri = "https://management.azure.com$resourceId/$action" + "?api-version=$apiVersion"

    Write-Output "🔧 Invoking '$action' on capacity..."
    Write-Output "📎 URI: $uri"

    try {
        Invoke-RestMethod -Method POST -Uri $uri -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
        Write-Output "✅ Action '$action' submitted successfully."
    } catch {
        Write-Output "❌ Failed to invoke action '$action': $_"
    }
}

switch ($state.ToLower()) {
    "paused" {
        Write-Output "▶ Capacity is paused. Resuming..."
        Invoke-CapacityAction -action "resume"
    }
    "succeeded" {
        Write-Output "⏸ Capacity is running. Pausing..."
        Invoke-CapacityAction -action "suspend"
    }
    default {
        Write-Output "⚠ Capacity is in an unknown state: $state. No action taken."
    }
}
