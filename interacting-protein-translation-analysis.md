---
description: >-
  I will be using bioinformatic approaches to analyze Translation Ratio and
  Efficiency between self-interacting proteins and non-self interacting
  proteins.
---

# Interacting Protein Translation Analysis

## PBerry\|07/27/2020&gt;

Process: generate a list of all known proteins, divided into self-polymerizing/interacting and non-self polymerizing/interacting. Run the analysis from the DD project. Primary difficulties I will need to address in my script: 

* Avoiding duplicating proteins
* Converting between UniprotKB/ensembl/refseqIDs

### Databases

* Database of Interacting Proteins: [https://dip.doe-mbi.ucla.edu/](https://dip.doe-mbi.ucla.edu/)
* Translatome Database: [http://www.translatomedb.net/](http://www.translatomedb.net/)

\|15:16 CDT&gt; The DIP doesn't have a robust search function - not sure what the difference between the different interaction types are.

\|17:49 CDT&gt; found this page! [https://dip.doe-mbi.ucla.edu/dip/Guide.cgi?SM=0:10](https://dip.doe-mbi.ucla.edu/dip/Guide.cgi?SM=0:10)

According to this any homo-oligomer is reported as "direct interaction"

From Soong et al, 2008, it seems that going for the "physical association" tag in the DIP database is best.

> Soong TT, Wrzeszczynski KO, Rost B. Physical protein-protein interactions predicted from microarrays. Bioinformatics. 2008;24\(22\):2608-2614. doi:10.1093/bioinformatics/btn498

### Strategy

* extract all entries from the DIP data table with uniprot IDs
* extract all entries from this data table with matching 0 and 1 entries
* if the interaction is classified as "direct interaction" put into a list of polymers
* put entries that don't make this list into a list of non-polymers

Testing for interaction types:

* "direct interaction" with only uniprotKB IDs = 32 hits
* uniprotKB ids with no interaction type specified = 508
* "physical association" with only uniprotKB IDs =  107
* only matching last 6 digits = 509

## PBerry\|07/28/2020&gt;

Lab meeting notes: RNAs forming prions?

motif for QXQ???QXQ strong bias that middle residue will be a glutamine also \(Q\)

### Testing DIP flat file for duplicates/omissions

Only found one DIP node \(DIP-29383N, maps to RAD51 in UniprotKB\) that did not have a Uniprot ID on the self-interacting entries for `Hsapi20170205.txt` There was a number of entries that mapped to  [Q06609](https://www.uniprot.org/uniprot/Q06609) in the file, none that mapped to any other RAD51 identifier in UniprotKB. So far it appears I can disregard any entries that do not have a UniprotKB ID.

Results from duplicate testing:

```text
Used proteins length: 508
Poly proteins length: 507
Unique poly proteins length: 507
No Uniprot id poly proteins length: 1
Used proteins length: 3421
Mono proteins length: 2913
Unique mono proteins length: 2913
No Uniprot id mono proteins length: 169
```

For non-poly proteins with no UniprotKBs OR RefSeq IDs, the proteins appear to be random polypeptides. For non-poly proteins with no UniprotKBs AND a RefSeq ID, the proteins appear to have all been removed from RefSeq.  
So far I have only spot-checked this.

DIP-61984N has a Zebrafish protein \(A0A0R4ISJ3\) ???? Made executive decision to omit that one.

## PBerry\|07/29/2020&gt;



