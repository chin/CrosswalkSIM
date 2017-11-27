#!/usr/bin/env bash

source "${SIMGRADING}/grader-lib.sh"

set -e

# the example runs (blue lines) on the wiki .../Answers page were generated with
# RUNS=300, so grading with RUNS=400 means students results should look *better*
# than the ../Answers page example plots.  If in doubt, run 
#  $ ./grader.sh . 9876 800
# which should definitly be comparatively closer to the CORRECT blue dots.
# NOTE:  the period as a first argument is needed when alternative SEEDS or N
#        are specified!
RUNS=${1:-400}
SEED=${2:-7654}
ARRIVALS=${3:-2000}
declare -a gslexec=( "${SIMGRADING}/gsl-make-trace" - u 0 1 )

if ! test -d "${SIMGRADING}" -a -x "${SIMGRADING}/gsl-make-trace" ; then
	echo >&2 "ERROR:  SIMGRADING or SIMGRADING/gsl-make-trace not found on system."
	echo >&2 "ERROR:  have you run setup.sh from grader-resources.tar.bz2 in your shell?"
	exit 1
fi

declare -a r=( 1 1 1 )
cat <<EoT |grader_msg 
Running SIM with non-existent trace file.  These runs should exit with non-zero
status and without OUTPUT lines...
EoT
set +e   # disregard exit status
echo ">> $S BEGIN Output <<" 
"${simloc}/SIM" 2000 /this/file/should/not/exist <("${gslexec[@]}" 1) <("${gslexec[@]}" 2)
r[0]=$?
echo '>> END   Output <<'
"${simloc}/SIM" 2000 <("${gslexec[@]}" 1) /this/file/should/not/exist <("${gslexec[@]}" 2)
r[1]=$?
echo '>> END   Output <<'
"${simloc}/SIM" 2000 <("${gslexec[@]}" 1) <("${gslexec[@]}" 2) /this/file/should/not/exist 
r[2]=$?
echo '>> END   Output <<'
echo ${simloc}/SIM exit status "(should be three non-zero values)" "${r[@]}"
echo
grader_keystroke


grader_msg <<EoT
Running SIM with truncated trace file.  These runs should exit with non-zero
status and without OUTPUT lines...
EoT
set +e   # disregard exit status
echo ">> $S BEGIN Output <<" 
"${simloc}/SIM" 2000 <("${gslexec[@]}" 3 |sed -n -e '1,10p') <("${gslexec[@]}" 1) <("${gslexec[@]}" 2)
r[0]=$?
echo '>> END   Output <<'
"${simloc}/SIM" 2000 <("${gslexec[@]}" 1) <("${gslexec[@]}" 3 |sed -n -e '1,10p') <("${gslexec[@]}" 2)
r[1]=$?
echo '>> END   Output <<'
"${simloc}/SIM" 2000 <("${gslexec[@]}" 1) <("${gslexec[@]}" 2) <("${gslexec[@]}" 3 |sed -n -e '1,10p') 
r[2]=$?
echo '>> END   Output <<'
echo ${simloc}/SIM exit status "(should be three non-zero values)" "${r[@]}"
echo
grader_keystroke


grader_msg <<EoT
Running many SIM experiments with varying seeds.  This may take 
some time ...
EoT
set -e
SIMS=crosswalksim
METRICS="dadat s2adat dpdat"
missingdata=0
for S in ${SIMS} ; do
	echo -n >&2 $S $RUNS " "
	for ((i=0, j=0; i<${RUNS}; i++, j+=3 )); do 
		test $(( $i % 100 )) -eq 0 && echo -n >&2 $i " "
		residualprefix="__residual-${S}"
		"${simloc}/SIM" ${ARRIVALS} \
				<("${gslexec[@]}" $(( SEED + j )) |tee "${residualprefix}-random_auto-run-$i.dat" )  \
				<("${gslexec[@]}" $(( SEED + j + 1 )) |tee "${residualprefix}-random-ped-run-$i.dat" )  \
				<("${gslexec[@]}" $(( SEED + j + 2 )) |tee "${residualprefix}-random_button-run-$i.dat" )  \
				| tee "${residualprefix}-output-run-${i}.log" \
				| "${SIMGRADING}/output-pipe" | tr '\n' ' '  | sed -e 30d -e 50d
		echo
	done | awk \
			-v dat1=__dadat-${S}-$SEED-$RUNS.dat \
			-v dat2=__s2adat-${S}-$SEED-$RUNS.dat \
			-v dat3=__dpdat-${S}-$SEED-$RUNS.dat \
			'{ print $1 >dat1; print $2 >dat2; print $3 >dat3; }'

	echo >&2
	grader_save_residuals ${S}

	grader_msg <<EoT
... generating comparison plots for ${S} ...
EoT
	for x in ${METRICS} ; do 
		runs=`sed -e '/^[[:space:]]*$/d' __${x}-${S}-$SEED-$RUNS.dat | wc -l |tr -d '[:space:]'`
		test ${runs} -ne ${RUNS} && missingdata=1	
		# generate plots from the *good* data results
		sed -e '/^[[:space:]]*$/d'  __${x}-${S}-$SEED-$RUNS.dat |\
			sort -n |${SIMGRADING}/cdf >_$x-${S}-$SEED-$RUNS.dat	
		gp=_$x-${S}-${SEED}-${RUNS}.gplot
		cat "${graderloc}/_${x}-${S}-plot.gplot" | sed \
				-e 's/\(title.*\)N=0\(.*\)/\1N='${runs}'\2/' \
				-e "s/_\([^-]*-[^-]*\)-0-0/_\1-$SEED-$RUNS/g" |\
			tee "${gp}" | cat >/dev/null
			gnuplot -d -e "set terminal pdf" -e 'set output "'${gp/gplot/pdf}'"' "${gp}"
	done
	if test ${missingdata} -eq 1 ; then 
		grader_missing_data $S $RUNS $SEED 231
	fi
done

grader_msg <<EoT
Inspect _*-$(grader_args2re ${SIMS})-*-*.pdf for 
submission results vs. rubric results.  See the comments at the top of this
script for borderline cases...
EoT

