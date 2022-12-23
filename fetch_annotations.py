#! /usr/bin/python

import requests
import sys
import os
import argparse
import time


def uniquify(path):
    #from https://stackoverflow.com/a/57896232
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + "_(" + str(counter) + ")" + extension
        counter += 1
    return path



def fetch(infile, outfile=None):
    # get accession IDs from infile
    with open(str(infile), "r") as accessions_file:
        IDlist = [line.rstrip() for line in accessions_file]
    
    # output is stored in ./data/gene_GO_annotations.txt unless specified
    if not outfile:
        if os.path.exists("gene_GO_annotations.txt"):
            outfile = uniquify("gene_GO_annotations.txt")
        else:
            outfile = "gene_GO_annotations.txt"


    # fetch annotations and write to file
    with open(outfile, "w") as annotations_file:
        for id in IDlist:
            requestURL = f"https://www.ebi.ac.uk/QuickGO/services/annotation/downloadSearch?geneProductId={id}%20&geneProductType=protein"
            r = requests.get(requestURL, headers={ "Accept" : "text/tsv"})

            # confirm HTTPS response
            if not r.ok:
                r.raise_for_status()
                sys.exit()

            annotations_file.write(r.text)

            # wait before next query
            time.sleep(5)

    print(f"Fetched Gene Ontologies, results stored in {outfile}")

def main():
    parser = argparse.ArgumentParser(
                    prog="fetch_annotations",
                    description="Fetches Gene ontology annotations of list of genes stored in -in--file from QuickGO and stores in -out--file")
    parser.add_argument("-in--file", help="filepath for file containing UniprotKB accession IDs", dest="infile", type=str, required=True)
    parser.add_argument("-out--file", help="Location to store file containing GO annotations", dest="outfile", type=str, required=False)
    parser.set_defaults(func=fetch)
    args = parser.parse_args()
    args.func(infile=args.infile, outfile=args.outfile)


if __name__=="__main__":
    main()
    
