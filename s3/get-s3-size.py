import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

# Create a reusable Paginator
paginator = s3.get_paginator('list_objects')

# iterate through all buckets
for bucket in response['Buckets']:
    try:
        # get bucket name
        buck = bucket["Name"]
        # create page iterator to get through all items inside a bucket
        page_iterator = paginator.paginate(Bucket=buck)
        # Create counters for item numbers, and item size
        big_counter = 0
        total_size = 0
        for response2 in page_iterator:
            if 'Contents' in response2:
                bucket_size = 0
                counter = 0
                for obj in response2['Contents']:
                    bucket_size += obj['Size']
                    counter += 1
                big_counter += counter
                total_size += bucket_size
            else:
                bucket_size = 0
        total_gb = total_size / 1024 / 1024 / 1024
        # print the result in csv format, to be able to re-use the information for further analysis
        print(buck + ', ' + str(round(total_gb, 2)) + ', ' + str(big_counter))
    # create exception in case you don't have access to a bucket
    except:
        # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        # message = template.format(type(ex).__name__, ex.args)
        # print(message)
        # raise
        continue
