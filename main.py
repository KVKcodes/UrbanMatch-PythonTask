from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import models, schemas
from database import SessionLocal, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check for existing email
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Convert interests list to comma-separated string for storage
        user_dict = user.dict()
        user_dict['interests'] = ','.join(user_dict['interests']) if user_dict['interests'] else ''
        
        db_user = models.User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Convert interests back to list before returning
        if isinstance(db_user.interests, str):
            db_user.interests = db_user.interests.split(',') if db_user.interests else []
        
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Please check your input."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    # Convert interests string to list before returning
    for user in users:
        if isinstance(user.interests, str):
            user.interests = user.interests.split(',') if user.interests else []
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert interests string to list before returning
    if isinstance(user.interests, str):
        user.interests = user.interests.split(',') if user.interests else []
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict(exclude_unset=True)
    if 'interests' in user_data and user_data['interests'] is not None:
        user_data['interests'] = ','.join(user_data['interests'])
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.get("/users/{user_id}/matches", response_model=List[schemas.User])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        # Get all users of opposite gender except the current user
        matches = db.query(models.User).filter(
            models.User.id != user_id,
            models.User.gender != user.gender
        ).all()
        
        # Get user's interests as a set for comparison
        user_interests = set(user.interests.split(',') if isinstance(user.interests, str) and user.interests else [])
        
        filtered_matches = []
        for match in matches:
            try:
                # Get match's interests as a set
                match_interests = set(match.interests.split(',') if isinstance(match.interests, str) and match.interests else [])
                
                # Check for common interests or same city
                common_interests = user_interests & match_interests
                same_city = user.city == match.city
                
                if common_interests or same_city:
                    match.interests = list(match_interests)
                    filtered_matches.append(match)
            
            except Exception as e:
                print(f"Error processing match {match.id}: {str(e)}")
                continue
        
        return filtered_matches
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

