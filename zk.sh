#!/bin/bash

function print_help() {
	printf "Usage: zk <command>\n"
	printf "new - create new note\n"
	printf "help - displays this help page\n"
	printf "index - indexes current notes and creates index pages\n"
	exit 0
}

function create_new_note() {
	DATE=`date "+%Y%m%d-%H%M%S"`
	printf "Enter file name: "

	read FILE_NAME

	if [[ "$FILE_NAME" == "end" ]]
	then
		exit 0
	fi

	FILE_NAME=${FILE_NAME//[[:space:]]/-}

	FILE_NAME=${DATE}-${FILE_NAME}.md

	printf "Begin typing note:\n>> "
	read NOTE
	printf "\nAdd tags (seperate tags by ','): "
	read TAG
	TAG=${TAG//[[:space:]]/}

	touch ${FILE_NAME}
	printf "[//]: ${FILE_NAME}\n" >> ${FILE_NAME}
	printf "# ${FILE_NAME}\n" >> ${FILE_NAME}
	printf "TAGS=$TAG\n" >> ${FILE_NAME}
	printf "### Begin Note>>>\n" >> ${FILE_NAME}
	printf "$NOTE" >> ${FILE_NAME}

	printf "\n"
	create_new_note
}

function remove_tags_folder() {
	if [[ -d ".tags" ]]
	then
		rm -r ".tags"
	fi
}

function create_tags() {
	remove_tags_folder
	printf "## Tags\n" >> index.md
	for FILE in ./*
	do
		if [[ "$FILE" == *".md"* ]]
		then
			FILE="${FILE//"./"/}"

			if [[ "$FILE" != "index.md" ]]
			then
				TAGS=$(grep "TAGS" $FILE)
				TAGS="${TAGS//"TAGS="/}"

				if [ -n $TAGS ]
				then
					IFS=',' read -ra SPLIT_TAGS <<< "$TAGS"

					for i in "${SPLIT_TAGS[@]}"
					do
						mkdir -p ".tags"
						touch .tags/$i.md
						printf "[$i](.tags/$i.md)  \n" >> index.md
						printf "[$FILE](../$FILE)  \n" >> .tags/$i.md
					done
				fi
			fi
		fi
	done
}

function make_index_file() {
	CURRENT_DIR="${PWD##*/}"

	touch index.md
	printf "# $CURRENT_DIR\n" > index.md
}

function index_files() {

	make_index_file
	
	for FILE in ./*
	do
		if [[ "$FILE" == *".md"* ]]
		then
			FILE="${FILE//"./"/}"

			if [[ "$FILE" != "index.md" ]]
			then
				printf "[$FILE]($FILE)  \n" >> index.md
			fi
		fi
		if [[ -d $FILE ]]
		then
			if [ "$(ls -A $FILE)" ]
			then
				cd $FILE
				index_files
				cd ..
			fi
		fi
	done
	printf "## Subdirectories\n" >> index.md
	for FILE in ./*
	do
		FILE="${FILE//"./"/}"
		if [[ -d $FILE ]]
		then
			if [ "$(ls -A $FILE)" ]
			then
				printf "[$FILE]($FILE/index.md)  \n" >> index.md
			fi
		fi
	done
	create_tags 0
}

if [ $# -eq 0 ]
then
printf "Type 'end' to stop making notes\n\n"
	create_new_note
fi

if [[ "$1" == "help" ]]
then
	print_help
fi

if [[ "$1" == "new" ]]
then
	create_new_note
fi

if [[ "$1" == "index" ]]
then
	index_files
fi

if [[ "$1" == "github" ]]
then
	mv index.md README.md
fi
