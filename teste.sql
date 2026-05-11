create table alunos (
id_aluno int identity (1,1) not null
,nome_aluno varchar (40) not null
constraint pk_aluno primary key (id_aluno)
)