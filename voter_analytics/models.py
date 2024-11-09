from django.db import models

# Create your models here.
class Voter(models.Model):
  ''' represents a voter'''
  last_name = models.TextField()
  first_name = models.TextField()
  address_st_num = models.IntegerField()
  address_name = models.TextField()
  address_apt_num = models.TextField()
  address_zip = models.IntegerField()
  dob = models.DateField(null=True)
  dor = models.DateField(null=True)
  party = models.TextField()
  precinct_num = models.TextField()
  v20state = models.TextField()
  v21town = models.TextField()
  v20primary = models.TextField()
  v22general = models.TextField()
  v23town = models.TextField()
  voter_score = models.IntegerField()

  def __str__(self):
    ''' str printout of voter '''
    return f'Voter: {self.first_name}{self.last_name}'
  
def load_data():
  ''' loads data into database '''

  # delete current data in database
  Voter.objects.all().delete()

  # open the file for reading:
  filename = 'C:/Users/mensu/Documents/newton_voters.csv'
  f = open(filename)
  headers = f.readline() # read/discard the headers
  # for each line in file
  for line in f:

    try:
        fields = line.split(',') # create a list of fields

        # create a new instance of Voter object with this record from CSV
        voter = Voter(last_name=fields[1],
                        first_name=fields[2],
                        address_st_num=fields[3],
                        address_name=fields[4],
                        address_apt_num=fields[5],
                        address_zip=fields[6],
                        dob=fields[7],
                        dor=fields[8],
                        party=fields[9].strip(),
                        precinct_num=fields[10],
                        v20state=fields[11],
                        v21town=fields[12],
                        v20primary=fields[13],
                        v22general=fields[14],
                        v23town=fields[15],
                        voter_score=fields[16],
                    )
        voter.save() # save this instance to the database.
        #print(f'Created result: {voter}')

    except Exception as e:
        print(f"Exception on {fields}, {e}")
  print("done")