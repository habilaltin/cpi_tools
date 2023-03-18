import pandas as pd

df = pd.read_csv("Zahlweg.csv", sep=";", dtype=str, encoding="utf-8")

lines = ""

for index, row in df.iterrows():
    lines += "<batchChangeSet><batchChangeSetPart><method>POST</method>"
    lines += "<YY1_PAYMENTMETHOD><YY1_PAYMENTMETHODType><Teilkonzern>{}</Teilkonzern><PaymentMethod_old>{}</PaymentMethod_old><PaymentMethod_new>{}</PaymentMethod_new></YY1_PAYMENTMETHODType></YY1_PAYMENTMETHOD>".format(row["Teilkonzern"], row["Zahlweg_alt"], row["Zahlweg_neu"])
    lines += "</batchChangeSetPart></batchChangeSet>\n"
    
csv = "<batchParts>" + lines + "</batchParts>"

with open('request_ready.txt', 'w') as f:
    f.write(csv)


#batch request structure:

#<batchParts>
#   <batchChangeSet>
#       <batchChangeSetPart>
#           <method>POST</method>
#           <YY1>
#               [...]
#           </YY1>
#       </batchChangeSetPart>
#   </batchChangeSet>
#</batchParts>