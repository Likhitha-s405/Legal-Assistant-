from rouge_score import rouge_scorer

# Example reference summary (human written)
reference = """
The charge created in respect of municipal property tax by section 212 of the City of Bombay Municipal Act, 1888, is an "annual charge not being a capital charge" within the mean ing of section 9 (1) (iv) of the Indian Income tax Act, 199.2, and the amount of such charge should therefore be deducted in computing the income from such property for the purposes of section 9 of the Indian Income tax Act.
The charge in respect of urban immoveable property tax created by the Bombay Finance Act, 1939 is similar in character and the amount of such charge should also be deducted.
The expression "capital charge" in s.9(1) (iv) means a charge created for a capital sum,that is to say, a charge created to. ' secure the discharge of a liability of a capi tal nature; and an "annual charge" means a charge to secure an annual liabili ty. 554
"""

# Your model generated summary
generated = """
The assessee company is an investment company deriving its income from properties in the city of Bombay.
For the assessment year 1940 41 the net income of the assessee under the head "property" was computed by the Income tax Officer in the sum of Rs. 6,21,764 after deducting from gross rents certain payments.
The company had paid during the relevant year Rs. 1,22,675 as municipal property tax and Rs. 32,760 as urban property tax.
Deduction of these two sums was claimed under the provisions of section 9 the Act.
Out of the first item a deduction in the sum of Rs. 48,572 was allowed on the ground that this item represented tenants'burdens paid by the assessee, otherwise the claim was disal lowed.
The, appeals of the assessee to the Appellate As sistant Commissioner and to the Income tax Appellate Tribu nal were unsuccessful.
The Tribunal, however, agreed to refer two questions of law to the High Court of Judicature at Bombay, namely, (1) Whether the municipal taxes paid by the applicant company are an allowable deduction under 555 the provisions of section 9 (1) (iv) of the Indian Income tax Act; (2) Whether the urban immoveable property taxes paid by the applicant company are an allowable deduction under section 9 (1) (iv) or under section 9 (1) (v) of
"""

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
scores = scorer.score(reference, generated)

for metric, score in scores.items():
    print(f"{metric}:")
    print(f"  Precision: {score.precision:.4f}")
    print(f"  Recall:    {score.recall:.4f}")
    print(f"  F1 Score:  {score.fmeasure:.4f}")
    print()