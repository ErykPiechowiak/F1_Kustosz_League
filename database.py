from sqlalchemy import create_engine, String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# 1. Baza (plik lokalnie)
engine = create_engine("sqlite:///f1_kustosz_league.db", echo=True)


# 2. Bazowa klasa ORM
class Base(DeclarativeBase):
    pass


# 3. Model tabeli
class RaceResult(Base):
    __tablename__ = "race_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    driver: Mapped[str] = mapped_column(String(50), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    race: Mapped[str] = mapped_column(String(100), nullable=False)

    position: Mapped[int] = mapped_column(Integer, nullable=False)
    gap_to_leader: Mapped[float] = mapped_column(Float)  # np. +12.345 sek
    points: Mapped[int] = mapped_column(Integer, nullable=False)


# 4. Tworzenie tabeli
#Base.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session

def main():
    with Session(engine) as session:
        result = RaceResult(
            driver="Bortoleto",
            team="Kick",
            race="Bahrain GP",
            position=1,
            gap_to_leader=2.2,
            points=18
        )

        session.add(result)
        session.commit()
        print("Dodano rekord")

if __name__ == "__main__":
    main()
#print("Baza i tabela utworzone")
