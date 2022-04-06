# ------------------------------------------
# Makefile for HGNC.owl
#
# History:
# - v1.1: with extra synonyms from PRO
# - v1.0: first version
# ------------------------------------------

HGNC2OWL=hgnc2owl
ROBOT=robot
CURL=curl

BUILD_DIR=build

EXTRAS=true

$(BUILD_DIR)/pro-markers.csv:
	if [ $(EXTRAS) = true ]; then $(CURL) -L https://docs.google.com/spreadsheets/d/1TYCEqBknmIITxp0pUUmQGR4Xx4IjSmVFqNYbgfY7syY/export\?format\=csv\&gid\=527460403 \
		--create-dirs -o $@ --retry 4 --max-time 200; fi

hgnc: $(BUILD_DIR)/pro-markers.csv
	$(HGNC2OWL) http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json \
		http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/withdrawn.json \
		-o $@.tmp.owl && \
	if [ $(EXTRAS) = true ]; then $(ROBOT) template --merge-before --input $@.tmp.owl \
			--template $^ \
			--prefix "HGNC: http://identifiers.org/hgnc/" \
			-o $@.tmp.owl; fi && \
	$(ROBOT) convert --input $@.tmp.owl --format ttl -o $@.tmp.owl.gz && \
	mv $@.tmp.owl $@.owl && \
	mv $@.tmp.owl.gz $@.owl.gz && \
	rm -f $(BUILD_DIR)/pro-markers.csv
.PRECIOUS: hgnc.owl hgnc.owl.gz
