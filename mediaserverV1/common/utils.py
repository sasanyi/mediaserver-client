from pathlib import Path
from mutagen.easyid3 import EasyID3
from sqlalchemy.exc import *

from common.models import *
from common.app import App
import re
from app.common.config import logger
import os

def findFilesInDirWithPattern(d, patterns):
    return [str(p.resolve()) for p in Path(d).glob("**/*") if p.suffix in patterns]


def saveMusicFileToDb(path):
    db = App.getDb().db
    file = db.query(File).where(File.path == re.escape(os.path.abspath(path))).one_or_none()
    if file is None:
        meta = Meta()
        try:
            audio = EasyID3(path)
            for key in audio.keys():
                setattr(meta, key, audio[key])
                if(type(audio[key]) is list):
                    setattr(meta, key, ",".join(audio[key]))

        except:
            pass
        finally:
            file = File(path=re.escape(os.path.abspath(path)), meta=meta)
            db.add(file)
            try:
                db.commit()
            except ProgrammingError as e:
                logger.error(str(type(e)) + " - " + str(e) + " - " + path + " - "+ str(e.statement) + " - "
                             + str(e.params))
                db.rollback()
            except OperationalError as e:
                logger.error(str(type(e)) + " - " + str(e) + " - " + path + " - " + str(e.statement) + " - "
                             + str(e.params))
                db.rollback()
            except SQLAlchemyError as e:
                logger.error(str(type(e)) + " - " + str(e) + " - " + path)
                db.rollback()


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    if total == 0:
        total = 1
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
