
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
})