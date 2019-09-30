SELECT * from party_sentiment;
#Get all rows = '86011'
SELECT tweet,sentiment FROM smdm.party_sentiment where sentiment= 'neg' and tweet like '%BJP4India%';
#Positive sentiment in BJP = 16259
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Bharatiya Janata Party" and num_sentiment = 1;
#Negative sentiment in BJP = 48102
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Bharatiya Janata Party" and num_sentiment = 0;
#Positive sentiment in INC = 3299
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Indian National Congress" and num_sentiment = 1;
#Negative sentiment in INC = 9320
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Indian National Congress" and num_sentiment = 0;
#INC = '12619', BJP = 64361
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Indian National Congress";
SELECT count(party_name) FROM smdm.party_sentiment where party_name ="Bharatiya Janata Party";
#look for american congress tweets which are incorrect = 548
SELECT count(party_name) FROM smdm.party_sentiment 
WHERE party_name ="Indian National Congress" 
AND (tweet LIKE '%trump%' OR tweet LIKE '%donald%' OR tweet LIKE '%u.s.%'  OR tweet LIKE '%potus%'OR tweet LIKE '%repub%' OR tweet LIKE '%democrat%'OR tweet LIKE '%nancy%');
#find rahul gandhi = '4078'
SELECT count(party_name) FROM smdm.party_sentiment 
WHERE party_name ="Indian National Congress" 
AND (tweet LIKE '%rahul%' OR tweet LIKE '%rahulgandhi%'OR tweet LIKE '%rahul gandhi%');
#find modi = '33391'
SELECT count(party_name) FROM smdm.party_sentiment 
WHERE party_name ="Bharatiya Janata Party" 
AND (tweet LIKE '%narendra%' OR tweet LIKE '%modi%');
#find type of source = 219 types
SELECT DISTINCT source from smdm.party_sentiment;