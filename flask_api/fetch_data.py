import couchdb
import csv
import json
# Connect to the CouchDB server and select a database
couch = couchdb.Server('http://admin:admin@localhost:5984/')
db = couch['tweet']
design_doc_name = '_design/mydesign'

#All Data View
view_func = '''function(doc) {
    if (doc.docs) {
        doc.docs.forEach(function(doc) {
            emit(null, doc);
        });
    }
}'''

# Create the view if it doesn't exist
view_name = 'All_Data'

if design_doc_name not in db:
    db[design_doc_name] = {
        'views': {
            view_name: {
                'map': view_func
            }
        }
    }
else:
    design_doc = db[design_doc_name]
    if view_name not in design_doc['views']:
        design_doc['views'][view_name] = {'map': view_func}
        db.save_doc(design_doc)


#Topics View
view_function = {
    "map": "function(doc) { if (doc.docs) { doc.docs.forEach(function(d) { emit(d.topic, 1); }); } }",
    "reduce": "function(keys, values) { return sum(values); }"
}

# Check if the design document exists
design_doc_id = design_doc_name
view_name_topic='topic_Data'
if design_doc_id in db:
    # Get the current revision of the design document
    design_doc = db[design_doc_id]
    current_rev = design_doc["_rev"]
    # Update the design document with the new view
    design_doc["views"][view_name_topic] = view_function
    db.save(design_doc, force_update=True, batch='ok', rev=current_rev)
else:
    # Create a new design document with the view
    design_doc = {
        "_id": design_doc_id,
        "views": {
            view_name_topic: view_function
        }
    }
    db.save(design_doc)

def save_topics():
        # Query the view
    result_topics = db.view(design_doc_name+'/_view/' + view_name_topic, group=True)
    result_dict = {row.key: row.value for row in result_topics}

    # Save the dictionary to a JSON file
    with open('../flask_api/static/data/result_topics.json', 'w') as jsonfile:
        json.dump(result_dict, jsonfile)
    # Print the results
    for row in result_topics:
        print(row.key, row.value)

    # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['value'])
    #     for row in result_topics:
    #         writer.writerow([row.value])



def save_all():
    # Query the view
    result_all = db.view(design_doc_name+'/_view/'  + view_name)

    # Print the first 5 rows of the results
    for i, row in enumerate(result_all):
        if i < 5:
            print(row.value)
        else:
            break
    # with open('../flask_api/static/data/results_all.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['value'])
    #     for row in result_all:
    #         writer.writerow([row.value])

    # Save the results to a JSON file
    with open('../flask_api/static/data/results_all.json', 'w') as jsonfile:
        json.dump([row.value for row in result_all], jsonfile)
    # Print the results
    # for row in result_all:
    #     print(row.value)