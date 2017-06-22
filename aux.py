import boto3
import time
import datetime
from dateutil.tz import tzlocal

stream_name = "test"
records_per_read = 100
timest = datetime.datetime(2016, 5, 26, 21, 29, 51, 30000)
initial_position = "TRIM_HORIZON" # or "LATEST"
sequence_number = "49563739517273067749522882060982940426021036387060416642"

def get_shard_iterators(kin):
	'''Function which gets iterators for all shards'''

	shard_ids = []
	stream = kin.describe_stream(StreamName=stream_name)

	for shard in stream["StreamDescription"]["Shards"]:

		shard_id = shard["ShardId"]

		# UTILIZAR SOLO UNO DE LOS SIGUIENTES ITERADORES. MANTENER EL RESTO COMENTADO
		# Shard Iterator por TrimHorizon o Latest
		shard_iterator = kin.get_shard_iterator(StreamName=stream_name, ShardIteratorType=initial_position, ShardId=shard_id)

		# Shard Iterator por SequenceNumber
		#shard_iterator = kin.get_shard_iterator(StreamName=stream_name, ShardIteratorType="AT_SEQUENCE_NUMBER", StartingSequenceNumber='49562325717353430662378673540711573757306106601036316722', ShardId=shard_id)

		# Shard Iterator por Timestamp
		#shard_iterator = kin.get_shard_iterator(StreamName=stream_name, ShardIteratorType="AT_TIMESTAMP", Timestamp=timest, ShardId=shard_id)

		shard_ids.append({'shard_id' : shard_id ,'shard_iterator' : shard_iterator['ShardIterator'] })

	return shard_ids


def main():
	kin = boto3.client('kinesis')

	shard_ids = get_shard_iterators(kin)

	#print shards_ids

	tries = 0

	while tries < 1000000:
		tries += 1

		msg = ""

		msg += "\n"
		msg += "######################################\n"
		msg += ">>>>>>>> Iteracion {0}\n".format(tries)

		for shard in shard_ids:
			msg += "\n"
			msg += ">>>>> {0}\n".format(shard["shard_id"])

			#Obten el primer elemento
			out = kin.get_records(ShardIterator=shard["shard_iterator"], Limit=records_per_read)

			if "NextShardIterator" in out:
				shard["shard_iterator"] = out["NextShardIterator"]

			msg += "Numero de registros: {}\n".format(len(out["Records"]))
			if len(out["Records"]) > 0:
				msg += "{}\n".format(out["Records"][0])

		msg += "######################################\n"
		msg += "\n"

		print msg

		time.sleep(2)
