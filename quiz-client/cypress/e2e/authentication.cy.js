
const login = () => {
  cy.intercept(
    'POST',
    '**/api/auth/login',
    {
      statusCode: 200,
      body: {
        'key': 'ACCESS_TOKEN'
      }
    }
  ).as('login');

  cy.visit('/login');
  cy.get('[data-cy=input-username]').type('test');
  cy.get('[data-cy=input-password]').type('test', { log: false });
  cy.get('button').contains('Login').click();
  cy.wait('@login');
}

describe('Authentication', () => {
  it('Can login', () => {
    login()    
    cy.location('pathname').should('eq', '/')
  })

  it('Cannot visit the login page when logged in.', function () {
    login()

    cy.visit('/login');
    cy.location('pathname').should('eq', '/');
  });

  it('Can sign up.', function () {
    cy.server();
    cy.route({
      method: 'POST',
      url: '**/api/auth/registration/',
      status: 201,
      response: {
        'key': '123456',
      }
    }).as('signUp');
  
    cy.visit('/signup');
    cy.get('[data-cy=input-username]').type('test');
    cy.get('[data-cy=input-email]').type('test@example.com');
    cy.get('[data-cy=input-password1]').type('pAssw0rd');
    cy.get('[data-cy=input-password2]').type('pAssw0rd');
    
    cy.get('button').contains('Create Account').click();
    cy.wait('@signUp');
    cy.location('pathname').should('eq', '/login');
  });

  it('Show invalid fields on sign up error.', function () {
    cy.server();
    cy.route({
      method: 'POST',
      url: '**/api/auth/registration/',
      status: 400,
      response: {
        'username': [
          'A user with that username already exists.'
        ]
      }
    }).as('signUp');
    cy.visit('/signup');
    cy.get('[data-cy=input-username]').type('test');
    cy.get('[data-cy=input-email]').type('test@example.com');
    cy.get('[data-cy=input-password1]').type('pAssw0rd');
    cy.get('[data-cy=input-password2]').type('pAssw0rd');;

    cy.get('button').contains('Create Account').click();
    cy.wait('@signUp');

    cy.get('span').contains(
      'A user with that username already exists'
    );

    cy.location('pathname').should('eq', '/signup');
    
  });

})