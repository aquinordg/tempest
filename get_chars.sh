clear

printf "\nGROUP OF CHARACTERS GENERATOR:\n\n"

printf "1. Single Group\n"
printf "2. Various Groups\n\n"

read -p "> Inform the option desired: "  choose
printf "\n"


if [ $choose == 1 ]; then
	clear
	printf "\nSINGLE GROUPS\n\n"
	
	read -p "> Select a seed (int): "  seed
	read -p "> Inform the size of group (int): "  n
	
	Rscript generate_characters.r -s $seed -n $n -o s${seed}n${n}.csv
	
elif [ $choose == 2 ]; then
	clear
	printf "\nVARIOUS GROUPS\n\n"

	read -p "> Inform the seeds of each group (int numbers divided by single space): " -a seed
	read -p "> Inform the size of each group (int numbers divided by single space, same length of seeds): " -a n
 
	for index in "${!seed[@]}"; do
		Rscript generate_characters.r -s ${seed[$index]} -n ${n[$index]} -o s${seed[$index]}n${n[$index]}.csv
	done
fi