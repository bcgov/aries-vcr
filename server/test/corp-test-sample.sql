
# different company types (BC, A, C, etc) "entity_type"

select distinct on (credential_json->'attributes'->>'entity_type') 
  corp_num, create_timestamp, credential_json->'attributes'->>'entity_type', credential_json->'attributes'->>'entity_name'
from hookable_cred
where credential_type = 'registration.registries.ca'
order by credential_json->'attributes'->>'entity_type', id desc;

# ACTive and HIStorical companies "entity_status"

select distinct on (credential_json->'attributes'->>'entity_status') 
  corp_num, create_timestamp, credential_json->'attributes'->>'entity_status', credential_json->'attributes'->>'entity_name'
from hookable_cred
where credential_type = 'registration.registries.ca'
order by credential_json->'attributes'->>'entity_status', id desc;

# BC and ex-pro companies (assumed name, home and remote jurisdiction) "entity_name", "assumed_name", "home_jurisdiction", "registered_jurisdiction"

select distinct on (credential_json->'attributes'->>'home_jurisdiction', credential_json->'attributes'->>'registered_jurisdiction') 
  corp_num, create_timestamp, credential_json->'attributes'->>'home_jurisdiction', credential_json->'attributes'->>'registered_jurisdiction', credential_json->'attributes'->>'entity_name'
from hookable_cred
where credential_type = 'registration.registries.ca'
order by credential_json->'attributes'->>'home_jurisdiction', credential_json->'attributes'->>'registered_jurisdiction', id desc;

# sole props (FM), DBA and owned-by companies "topic_relationship"

select distinct on (credential_json->'attributes'->>'relationship') 
  corp_num, create_timestamp, credential_json->'attributes'->>'relationship', credential_json->'attributes'->>'associated_registration_id'
from hookable_cred
where credential_type = 'relationship.registries.ca'
order by credential_json->'attributes'->>'relationship', id desc;

# large number of credentials "select count(*) from credential_set group by topic_id"

select id, source_id from topic where id in (
select topic_id from (
select topic_id, count(*) count from credential_set group by topic_id
order by count desc limit 2
) as foo);

# large number of relationships (Telus, Pattison) "select count(*) from credential_set group by topic_id"

select id, source_id from topic where id in (
select topic_id from (
select topic_id, count(*) count from topic_relationship group by topic_id
order by count desc limit 2
) as foo);

# name change, status change, short duration credentials

select id, source_id from topic where id in (
select topic_id from (
select topic_id, count(*) count from credential
where credential_type_id = 1
group by topic_id
order by count desc limit 5
) as foo);

# other credentials - BN, Cannabis license

select id, source_id from topic where id in (
select topic_id from (
select distinct on (credential_type_id) topic_id from credential
order by credential_type_id
) as foo);
