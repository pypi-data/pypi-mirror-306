import boto3
from datetime import datetime, timedelta
from collections import defaultdict

def get_service_details(client, start, end, service, group_by_key):
    """Get detailed breakdown for a specific service"""
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start.strftime('%Y-%m-%d'),
                'End': end.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': [service]
                }
            },
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': group_by_key}
            ]
        )
        return response['ResultsByTime'][0]['Groups']
    except Exception:
        return []

def get_aws_costs():
    client = boto3.client('ce')
    end = datetime.now()
    start = (end - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    
    # Get service level costs
    service_response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start.strftime('%Y-%m-%d'),
            'End': end.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'}
        ]
    )
    
    # Get detailed breakdowns for major services
    service_details = defaultdict(list)
    service_mappings = {
        'Amazon Elastic Compute Cloud - Compute': ('INSTANCE_TYPE', 'EC2'),
        'Amazon Simple Storage Service': ('USAGE_TYPE', 'S3'),
        'Amazon Relational Database Service': ('USAGE_TYPE', 'RDS'),
        'Amazon ElastiCache': ('USAGE_TYPE', 'ElastiCache'),
        'Amazon Simple Queue Service': ('USAGE_TYPE', 'SQS'),
        'AWS Lambda': ('USAGE_TYPE', 'Lambda')
    }
    
    for service in service_mappings:
        details = get_service_details(
            client, 
            start, 
            end, 
            service, 
            service_mappings[service][0]
        )
        if details:
            service_details[service_mappings[service][1]] = details
    
    return service_response, service_details, start.strftime('%Y-%m-%d')

def format_cost(cost):
    """Format cost with appropriate unit"""
    if cost >= 100:
        return f"${cost:.0f}"
    elif cost >= 10:
        return f"${cost:.1f}"
    else:
        return f"${cost:.2f}"

def create_bar_chart(costs, max_width=50):
    """Create a horizontal bar chart with given costs"""
    if not costs:
        return
    
    max_cost = max(cost for _, cost in costs)
    max_label_length = max(len(label) for label, _ in costs)
    
    # Print header
    total = sum(cost for _, cost in costs)
    print(f"\nTotal: {format_cost(total)}/day")
    print("-" * (max_width + max_label_length + 15))
    if max_cost == 0:
        return
    
    # Print bars
    for label, cost in costs:
        # Calculate bar width
        width = int((cost / max_cost) * max_width)
        bar = "█" * width
        
        # Format the line with cost and percentage
        percentage = (cost / total) * 100
        label_padded = label.ljust(max_label_length)
        cost_formatted = format_cost(cost).rjust(8)
        print(f"{label_padded} {cost_formatted}/day ({percentage:5.1f}%) {bar}")

def main():
    try:
        print("Fetching AWS cost data...")
        service_data, service_details, date = get_aws_costs()
        
        print(f"\nAWS Cost Analysis for {date}")
        print("=" * 50)
        
        # Prepare service level data
        service_costs = [
            (group['Keys'][0].replace('Amazon ', '').replace('AWS ', ''),
             float(group['Metrics']['UnblendedCost']['Amount']))
            for group in service_data['ResultsByTime'][0]['Groups']
        ]
        service_costs.sort(key=lambda x: x[1], reverse=True)
        
        # Print main service breakdown
        print("\nCost by Service:")
        create_bar_chart(service_costs)
        
        # Print detailed breakdowns for major services
        for service, details in service_details.items():
            if details:
                print(f"\n{service} Breakdown:")
                detailed_costs = [
                    (group['Keys'][0].split(':')[-1],
                     float(group['Metrics']['UnblendedCost']['Amount']))
                    for group in details
                ]
                detailed_costs.sort(key=lambda x: x[1], reverse=True)
                create_bar_chart(detailed_costs)
                
                # Print projected monthly cost for the service
                daily_total = sum(cost for _, cost in detailed_costs)
                monthly_projected = daily_total * 30.5
                print(f"Projected monthly {service} cost: {format_cost(monthly_projected)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPlease ensure you have:")
        print("1. AWS credentials configured")
        print("2. Required permissions for Cost Explorer")
        print("3. boto3 installed (pip install boto3)")

if __name__ == "__main__":
    main()
